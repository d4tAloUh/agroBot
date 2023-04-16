from tgbot.handlers.sale_detail.manage_data import DELETE_SALE_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_delete_sale_callback_data(sale_id: int) -> str:
    return f"{DELETE_SALE_CALLBACK}{callback_separator}{sale_id}"
