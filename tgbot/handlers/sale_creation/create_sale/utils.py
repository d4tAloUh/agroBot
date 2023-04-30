from tgbot.handlers.menu.manage_data import MENU_CALLBACK_DATA
from tgbot.handlers.sale_creation.create_sale.manage_data import ACCEPT_SALE_CALLBACK
from tgbot.handlers.sale_creation.price_type.manage_data import CHOOSE_PRICE_TYPE_CALLBACK


def get_go_back_from_sale_preview_callback_data() -> str:
    return f"{CHOOSE_PRICE_TYPE_CALLBACK}"


def get_accept_sale_callback_data() -> str:
    return f"{ACCEPT_SALE_CALLBACK}"


def get_decline_sale_callback_data() -> str:
    return f"{MENU_CALLBACK_DATA}"
