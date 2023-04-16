from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.sale_creation.product.utils import get_choose_product_callback_data
from tgbot.handlers.sales.utils import get_choose_sale_callback_data


def make_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            static_text.create_new_sale_text,
            callback_data=get_choose_product_callback_data(page=1)
        )],
        [InlineKeyboardButton(
            static_text.my_sales_text,
            callback_data=get_choose_sale_callback_data(page=1)
        )]
    ]

    return InlineKeyboardMarkup(buttons)
