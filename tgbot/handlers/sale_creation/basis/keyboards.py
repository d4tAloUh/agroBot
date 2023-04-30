from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.sale_creation.city.utils import get_choose_city_callback_data
from tgbot.handlers.sale_creation.basis import static_text


def make_select_basis_keyboard(text: str, callback_data: str) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            text,
            callback_data=callback_data
        ),
    ]]

    return InlineKeyboardMarkup(buttons)
