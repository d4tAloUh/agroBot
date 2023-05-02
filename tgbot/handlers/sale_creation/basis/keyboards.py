from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.sale_creation.basis.utils import get_select_basis_callback_data
from tgbot.handlers.sale_creation.city.utils import get_choose_city_callback_data
from tgbot.handlers.sale_creation.basis import static_text


def make_select_basis_keyboard(text: str, callback_data: str) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            static_text.select_elevator_text,
            callback_data=get_select_basis_callback_data(static_text.select_elevator_text)
        ),
        InlineKeyboardButton(
            static_text.select_farm_text,
            callback_data=get_select_basis_callback_data(static_text.select_farm_text)
        ),
    ],[
        InlineKeyboardButton(
            text,
            callback_data=callback_data
        ),
    ]]

    return InlineKeyboardMarkup(buttons)
