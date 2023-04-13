from django.core.paginator import Paginator
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import SubRegion
from tgbot.handlers.sale_creation.city.handlers import callback_city_choosing
from tgbot.handlers.sale_creation.region.utils import get_choose_region_callback_data
from tgbot.handlers.sale_creation.subregion import static_text
from tgbot.handlers.sale_creation.subregion.utils import get_subregion_chosen_callback_data, get_choose_subregion_callback_data
from tgbot.handlers.utils.helpers import extract_page, extract_id
from tgbot.handlers.utils.keyboards import make_paginated_keyboard


def callback_subregion_chosen(update: Update, context: CallbackContext) -> None:
    subregion_id = extract_id(update.callback_query.data)
    # Save selected product id
    context.user_data["subregion_id"] = subregion_id
    # Call next step
    update.callback_query.data = get_choose_subregion_callback_data(1)
    callback_city_choosing(update, context)


def callback_subregion_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.SUBREGION_STEP_NAME

    region_id = context.user_data.get("region_id")
    # TODO: handle region id being none (skip to choose product)

    subregions = SubRegion.objects.all()
    if region_id:
        subregions = subregions.filter(region_id=region_id)
    paginator = Paginator(
        object_list=subregions,
        per_page=static_text.subregion_per_row * static_text.subregion_rows
    )

    page = extract_page(update.callback_query.data)
    products_page = paginator.get_page(page)
    keyboard = make_paginated_keyboard(
        items=products_page.object_list,
        page=page,
        is_last_page=not products_page.has_next(),
        get_item_callback=get_subregion_chosen_callback_data,
        prev_page_callback=get_choose_subregion_callback_data(page - 1),
        next_page_callback=get_choose_subregion_callback_data(page + 1),
        go_back_callback=get_choose_region_callback_data(1),
        go_back_text=static_text.go_back_text
    )
    update.callback_query.edit_message_text(
        static_text.choose_subregion_text,
        reply_markup=keyboard
    )

