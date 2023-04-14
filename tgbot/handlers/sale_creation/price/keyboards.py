from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.sale_creation.price import static_text
from tgbot.handlers.sale_creation.price.utils import get_go_back_from_input_price_callback_data


def make_input_price_keyboard() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            static_text.go_back_to_input_basis,
            callback_data=get_go_back_from_input_price_callback_data()
        ),
    ]]

    return InlineKeyboardMarkup(buttons)
