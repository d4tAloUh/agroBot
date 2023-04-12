from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.sale_creation.product.utils import get_choose_product_callback_data
from tgbot.handlers.sale_creation.weight import static_text


def make_select_weight_keyboard() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            static_text.go_back_to_choose_product,
            callback_data=get_choose_product_callback_data(page=1)
        ),
    ]]

    return InlineKeyboardMarkup(buttons)
