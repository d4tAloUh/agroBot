from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.sale_creation.city.utils import get_choose_city_callback_data
from tgbot.handlers.sale_creation.basis import static_text


def make_select_basis_keyboard() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            static_text.go_back_to_choose_city,
            callback_data=get_choose_city_callback_data(page=1)
        ),
    ]]

    return InlineKeyboardMarkup(buttons)
