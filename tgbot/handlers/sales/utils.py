from sales.models import Product, SalesPlacement
from tgbot.handlers.menu.manage_data import MENU_CALLBACK_DATA
from tgbot.handlers.sales.manage_data import CHOOSE_SALE_CALLBACK, SALE_CHOSEN_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_sale_button_text(sale: SalesPlacement) -> str:
    return f"#{sale.pk} - {sale.product.name}"


def get_sale_chosen_callback_data(sale: SalesPlacement) -> str:
    return f"{SALE_CHOSEN_CALLBACK}{callback_separator}{sale.pk}"


def get_choose_sale_callback_data(page: int) -> str:
    return f"{CHOOSE_SALE_CALLBACK}{callback_separator}{page}"


def get_go_back_from_choose_sale_callback_data() -> str:
    return f"{MENU_CALLBACK_DATA}"
