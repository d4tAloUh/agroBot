from sales.models import Region
from tgbot.handlers.sale_creation.region.manage_data import CHOOSE_REGION_CALLBACK, REGION_CHOSEN_CALLBACK
from tgbot.handlers.sale_creation.weight.manage_data import INPUT_WEIGHT_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_region_chosen_callback_data(region: dict) -> str:
    return f"{REGION_CHOSEN_CALLBACK}{callback_separator}{region['pk']}{callback_separator}{region['city']}"


def get_choose_region_callback_data(page: int) -> str:
    return f"{CHOOSE_REGION_CALLBACK}{callback_separator}{page}"


def get_go_back_from_choose_region_callback_data() -> str:
    return f"{INPUT_WEIGHT_CALLBACK}"
