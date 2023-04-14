from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.sale_creation.create_sale import static_text
from tgbot.handlers.sale_creation.create_sale.utils import get_go_back_from_sale_preview_callback_data, \
    get_accept_sale_callback_data, get_decline_sale_callback_data


def make_sales_preview_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        # 1st row
        [
            InlineKeyboardButton(
                static_text.accept_sale_text,
                callback_data=get_accept_sale_callback_data()
            ),
            InlineKeyboardButton(
                static_text.cancel_sale_text,
                callback_data=get_decline_sale_callback_data()
            ),
        ],
        # 2nd row
        [
            InlineKeyboardButton(
                static_text.go_back_to_price_type_select_text,
                callback_data=get_go_back_from_sale_preview_callback_data()
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)
