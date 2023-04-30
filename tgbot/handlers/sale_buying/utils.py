from typing import List

from sales.models import Product
from tgbot.handlers.menu.manage_data import MENU_CALLBACK_DATA
from tgbot.handlers.sale_buying.manage_data import CHOOSE_PRODUCT_INTEREST_CALLBACK, PRODUCT_INTEREST_CHOSEN_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_product_interest_chosen_callback_data_function(page, interests):
    def get_product_interest_chosen_callback_data(product: Product) -> str:
        toggle_value = product.pk not in interests
        return f"{CHOOSE_PRODUCT_INTEREST_CALLBACK}{callback_separator}{page}{callback_separator}{product.pk}{callback_separator}{toggle_value}"
    return get_product_interest_chosen_callback_data


def get_choose_product_interest_callback_data(page: int):
    return f"{CHOOSE_PRODUCT_INTEREST_CALLBACK}{callback_separator}{page}"


def get_product_interest_text_function(interests):
    def get_product_interest_text(product: Product) -> str:
        interest_emoji = ''
        if product.pk in interests:
            interest_emoji = '✅ '
        return f"{interest_emoji}{product.name}"
    return get_product_interest_text


def get_go_back_from_choose_product_interest_callback_data():
    return f"{MENU_CALLBACK_DATA}"
