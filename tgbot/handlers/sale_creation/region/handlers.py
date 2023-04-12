from django.core.paginator import Paginator
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import Region
from tgbot.handlers.sale_creation.region import static_text
from tgbot.handlers.sale_creation.region.utils import get_region_chosen_callback_data, get_choose_region_callback_data, \
    get_go_back_from_choose_region_callback_data
from tgbot.handlers.sale_creation.subregion.handlers import callback_subregion_choosing
from tgbot.handlers.sale_creation.subregion.utils import get_choose_subregion_callback_data
from tgbot.handlers.utils.helpers import extract_page, extract_id
from tgbot.handlers.utils.keyboards import make_paginated_keyboard


def callback_region_chosen(update: Update, context: CallbackContext) -> None:
    region_id = extract_id(update.callback_query.data)
    # Save selected product id
    context.user_data["region_id"] = region_id
    # Call next step
    update.callback_query.data = get_choose_subregion_callback_data(1)
    callback_subregion_choosing(update, context)


def callback_region_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.REGION_STEP_NAME

    regions = Region.objects.all()
    paginator = Paginator(
        object_list=regions,
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
        context.bot.send_message(
            update.effective_chat.id,
            static_text.choose_region_text,
            reply_markup=keyboard
        )
