from sales.models import City
from tgbot.handlers.sale_creation.city.manage_data import CITY_CHOSEN_CALLBACK, CHOOSE_CITY_CALLBACK
from tgbot.handlers.utils.static_text import callback_separator


def get_city_chosen_callback_data(city: City) -> str:
    return f"{CITY_CHOSEN_CALLBACK}{callback_separator}{city.pk}"


def get_choose_city_callback_data(page: int) -> str:
    return f"{CHOOSE_CITY_CALLBACK}{callback_separator}{page}"
