from tgbot.handlers.sale_creation.currency.manage_data import CHOOSE_CURRENCY_CALLBACK
from tgbot.handlers.sale_creation.price_type.manage_data import CHOSEN_PRICE_TYPE_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_chosen_price_type_callback_data(price_type: str) -> str:
    return f"{CHOSEN_PRICE_TYPE_CALLBACK}{callback_separator}{price_type}"


def get_go_back_from_choose_price_type_callback_data() -> str:
    return f"{CHOOSE_CURRENCY_CALLBACK}"
