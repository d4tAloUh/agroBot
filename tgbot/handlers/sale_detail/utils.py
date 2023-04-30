from tgbot.handlers.sale_detail.manage_data import DELETE_SALE_CALLBACK, CONFIRM_DELETE_SALE_CALLBACK
from tgbot.handlers.sale_list.manage_data import SALE_CHOSEN_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_delete_sale_callback_data(sale_id: int) -> str:
    return f"{DELETE_SALE_CALLBACK}{callback_separator}{sale_id}"


def get_confirm_delete_sale_callback_data(sale_id: int) -> str:
    return f"{CONFIRM_DELETE_SALE_CALLBACK}{callback_separator}{sale_id}"


def get_go_back_from_confirmation(sale_id: int) -> str:
    return f"{SALE_CHOSEN_CALLBACK}{callback_separator}{sale_id}"
