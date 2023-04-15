from tgbot.handlers.sale_creation.price_type.manage_data import CHOOSE_PRICE_TYPE_CALLBACK
from tgbot.handlers.sale_creation.vat.manage_data import CHOSEN_VAT_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_chosen_vat_callback_data(price_type: str) -> str:
    return f"{CHOSEN_VAT_CALLBACK}{callback_separator}{price_type}"


def get_go_back_from_choose_vat_callback_data() -> str:
    return f"{CHOOSE_PRICE_TYPE_CALLBACK}"
