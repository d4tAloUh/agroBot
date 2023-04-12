from sales.models import Region
from tgbot.handlers.sale_creation.subregion.manage_data import SUBREGION_CHOSEN_CALLBACK, CHOOSE_SUBREGION_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_subregion_chosen_callback_data(region: Region) -> str:
    return f"{SUBREGION_CHOSEN_CALLBACK}{callback_separator}{region.pk}"


def get_choose_subregion_callback_data(page: int) -> str:
    return f"{CHOOSE_SUBREGION_CALLBACK}{callback_separator}{page}"
