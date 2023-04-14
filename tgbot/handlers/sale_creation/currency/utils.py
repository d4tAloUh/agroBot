from tgbot.handlers.sale_creation.price.manage_data import INPUT_PRICE_CALLBACK
from tgbot.handlers.sale_creation.currency.manage_data import CHOSEN_CURRENCY_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_chosen_currency_callback_data(currency: str) -> str:
    return f"{CHOSEN_CURRENCY_CALLBACK}{callback_separator}{currency}"


def get_go_back_from_choose_currency_callback_data() -> str:
    return f"{INPUT_PRICE_CALLBACK}"
