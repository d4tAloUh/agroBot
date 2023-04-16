from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.sale_detail import static_text
from tgbot.handlers.sale_detail.utils import get_delete_sale_callback_data
from tgbot.handlers.sales.utils import get_choose_sale_callback_data


def make_sale_detail_keyboard(sale_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            static_text.delete_sale_text,
            callback_data=get_delete_sale_callback_data(sale_id)
        )],
        [InlineKeyboardButton(
            static_text.go_back_from_sale_detail_text,
            callback_data=get_choose_sale_callback_data(page=1)
        )]
    ]

    return InlineKeyboardMarkup(buttons)
