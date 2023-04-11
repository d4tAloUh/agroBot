from django.core.paginator import Paginator
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import Product
from tgbot.handlers.sale_creation.product.utils import get_product_chosen_callback_data, \
    get_choose_product_callback_data, get_go_back_from_choose_product_callback_data
from tgbot.handlers.utils.helpers import extract_page
from users.models import TelegramUser
from tgbot.handlers.sale_creation.product import static_text
from tgbot.handlers.utils.keyboards import make_paginated_keyboard

def callback_product_choosing_cancel(update: Update, context: CallbackContext) -> None:
    pass




def callback_product_choosing(update: Update, context: CallbackContext) -> None:
    # u = TelegramUser.get_user(update, context)

    products = Product.objects.all()
    page = extract_page(update.callback_query.data)
    paginator = Paginator(
        object_list=products,
        per_page=static_text.products_per_row * static_text.product_rows
    )
    products_page = paginator.get_page(page)
    keyboard = make_paginated_keyboard(
        items = products_page.object_list,
        page=page,
        is_last_page=not products_page.has_next(),
        get_item_callback=get_product_chosen_callback_data,
        prev_page_callback=get_choose_product_callback_data(page - 1),
        next_page_callback=get_choose_product_callback_data(page + 1),
        go_back_callback=get_go_back_from_choose_product_callback_data(),
        go_back_text=static_text.go_back_text
    )
    update.callback_query.edit_message_text(
        static_text.choose_product_text,
        reply_markup=keyboard
    )
