from django.core.paginator import Paginator
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import SubRegion, City
from tgbot.handlers.sale_creation.subregion.utils import get_choose_subregion_callback_data
from tgbot.handlers.sale_creation.city import static_text
from tgbot.handlers.sale_creation.city.utils import get_choose_city_callback_data, get_city_chosen_callback_data
from tgbot.handlers.utils.helpers import extract_page, extract_id
from tgbot.handlers.utils.keyboards import make_paginated_keyboard


def callback_city_chosen(update: Update, context: CallbackContext) -> None:
    city_id = extract_id(update.callback_query.data)
    # Save selected product id
    context.user_data["city_id"] = city_id
    context.bot.send_message(
        update.effective_chat.id,
        "ВСЬО"
    )
    print(context.user_data)
    # # Call next step


def callback_city_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.CITY_STEP_NAME

    subregion_id = context.user_data.get("subregion_id")
    # TODO: handle subregion id being none (skip to choose product)

    cities = City.objects.all()
    if subregion_id:
        cities = cities.filter(subregion_id=subregion_id)
    paginator = Paginator(
        object_list=cities,
        per_page=static_text.cities_per_row * static_text.cities_rows
    )

    page = extract_page(update.callback_query.data)
    products_page = paginator.get_page(page)
    keyboard = make_paginated_keyboard(
        items=products_page.object_list,
        page=page,
        is_last_page=not products_page.has_next(),
        get_item_callback=get_city_chosen_callback_data,
        prev_page_callback=get_choose_city_callback_data(page - 1),
        next_page_callback=get_choose_city_callback_data(page + 1),
        go_back_callback=get_choose_subregion_callback_data(1),
        go_back_text=static_text.go_back_text
    )
    update.callback_query.edit_message_text(
        static_text.choose_city_text,
        reply_markup=keyboard
    )

