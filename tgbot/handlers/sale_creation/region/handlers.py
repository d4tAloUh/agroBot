from django.core.paginator import Paginator
from django.db.models import Value
from telegram import Update, Message
from telegram.ext import CallbackContext

from sales.models import Region, City
from tgbot.handlers.sale_creation.basis.handlers import callback_basis_input
from tgbot.handlers.sale_creation.region import static_text
from tgbot.handlers.sale_creation.region.utils import get_region_chosen_callback_data, get_choose_region_callback_data, \
    get_go_back_from_choose_region_callback_data
from tgbot.handlers.sale_creation.subregion.handlers import callback_subregion_choosing
from tgbot.handlers.sale_creation.subregion.utils import get_choose_subregion_callback_data
from tgbot.handlers.utils.helpers import extract_page, extract_id, delete_inline_keyboard_on_previous_inline_message, \
    extract_is_city
from tgbot.handlers.utils.keyboards import make_paginated_keyboard


def callback_region_chosen(update: Update, context: CallbackContext) -> None:
    entity_id = extract_id(update.callback_query.data)
    is_city = extract_is_city(update.callback_query.data)
    if is_city == 'True':
        # Save selected product id
        context.user_data["city_id"] = entity_id
        # Call next step
        callback_basis_input(update, context)
    else:
        # Save selected product id
        context.user_data["region_id"] = entity_id

        # Call next step
        update.callback_query.data = get_choose_subregion_callback_data(1)
        callback_subregion_choosing(update, context)


def callback_region_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.REGION_STEP_NAME

    regions = Region.objects.annotate(
        city=Value(False)
    ).values("pk", "name", "city")
    cities = City.objects.filter(
        region__isnull=True,
        subregion__isnull=True
    ).annotate(city=Value(True)).values("pk", "name", "city")
    results = cities.union(regions).order_by("-city", "name")
    paginator = Paginator(
        object_list=results,
        per_page=static_text.region_per_row * static_text.region_rows
    )

    if update.callback_query:
        # Coming from pagination or next step
        page = extract_page(update.callback_query.data)
    else:
        page = 1
    products_page = paginator.get_page(page)
    keyboard = make_paginated_keyboard(
        items=products_page.object_list,
        page=page,
        item_text_getter=lambda x: x["name"],
        is_last_page=not products_page.has_next(),
        get_item_callback=get_region_chosen_callback_data,
        prev_page_callback=get_choose_region_callback_data(page - 1),
        next_page_callback=get_choose_region_callback_data(page + 1),
        go_back_callback=get_go_back_from_choose_region_callback_data(),
        go_back_text=static_text.go_back_text
    )
    if update.callback_query:
        update.callback_query.edit_message_text(
            static_text.choose_region_text,
            reply_markup=keyboard
        )
    else:
        message: Message = context.bot.send_message(
            update.effective_chat.id,
            static_text.choose_region_text,
            reply_markup=keyboard
        )
        delete_inline_keyboard_on_previous_inline_message(
            update, context
        )
        context.user_data["last_message_with_inline"] = message.message_id
