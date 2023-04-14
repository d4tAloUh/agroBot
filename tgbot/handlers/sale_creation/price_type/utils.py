from tgbot.handlers.sale_creation.price.manage_data import INPUT_PRICE_CALLBACK
from tgbot.handlers.sale_creation.price_type.manage_data import CHOOSE_PRICE_TYPE_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_choose_price_type_callback_data(price_type: int) -> str:
    return f"{CHOOSE_PRICE_TYPE_CALLBACK}{callback_separator}{price_type}"


def get_go_back_from_choose_price_type_callback_data() -> str:
    return f"{INPUT_PRICE_CALLBACK}"
