from sales.models import Product
from tgbot.handlers.sale_creation.product.manage_data import PRODUCT_CHOSEN_CALLBACK, CHOOSE_PRODUCT_CALLBACK, \
    CANCEL_CHOOSE_PRODUCT_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_product_chosen_callback_data(product: Product) -> str:
    return f"{PRODUCT_CHOSEN_CALLBACK}{callback_separator}1{callback_separator}{product.pk}"


def get_choose_product_callback_data(page: int) -> str:
    return f"{CHOOSE_PRODUCT_CALLBACK}{callback_separator}{page}"


def get_go_back_from_choose_product_callback_data() -> str:
    return f"{CANCEL_CHOOSE_PRODUCT_CALLBACK}"
