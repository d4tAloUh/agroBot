from sales.models import Product
from tgbot.handlers.menu.manage_data import MENU_CALLBACK_DATA
from tgbot.handlers.sale_creation.product.manage_data import PRODUCT_CHOSEN_CALLBACK, CHOOSE_PRODUCT_CALLBACK, \
    GO_BACK_FROM_PRODUCT_TYPE_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_product_chosen_callback_data(product_or_type: dict) -> str:
    return f"{PRODUCT_CHOSEN_CALLBACK}{callback_separator}{product_or_type['pk']}{callback_separator}{product_or_type['is_product']}"


def get_choose_product_callback_data(page: int) -> str:
    return f"{CHOOSE_PRODUCT_CALLBACK}{callback_separator}{page}"


def get_go_back_from_choose_product_callback_data() -> str:
    return f"{MENU_CALLBACK_DATA}"


def get_go_back_from_product_type_callback_data() -> str:
    return f"{GO_BACK_FROM_PRODUCT_TYPE_CALLBACK}"
