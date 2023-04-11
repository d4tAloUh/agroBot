from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.sale_creation.product.utils import get_choose_product_callback_data


def make_keyboard_for_start_registered_user() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            static_text.create_new_sale_text,
            callback_data=get_choose_product_callback_data(page=1)
        ),
    ]]

    return InlineKeyboardMarkup(buttons)
