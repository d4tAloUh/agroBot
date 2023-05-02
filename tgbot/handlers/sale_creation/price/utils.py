from tgbot.handlers.sale_creation.basis.manage_data import CHOOSE_BASIS_CALLBACK
from tgbot.handlers.sale_creation.price_type.manage_data import CHOOSE_PRICE_TYPE_CALLBACK


def get_go_back_from_input_price_callback_data() -> str:
    return f"{CHOOSE_PRICE_TYPE_CALLBACK}"
