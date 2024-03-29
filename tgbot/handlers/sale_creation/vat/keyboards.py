from typing import Type

from django.db import models
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.sale_creation.vat import static_text
from tgbot.handlers.sale_creation.vat.utils import get_go_back_from_choose_vat_callback_data, \
    get_chosen_vat_callback_data


def make_choose_vat_keyboard(price_types: Type[models.TextChoices]) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for price_type in price_types:
        row.append(InlineKeyboardButton(
            price_types[price_type.upper()].label,
            callback_data=get_chosen_vat_callback_data(price_type)
        ))
    buttons.append(row)
    buttons.append([
        InlineKeyboardButton(
            static_text.go_back_to_price_type,
            callback_data=get_go_back_from_choose_vat_callback_data()
        )
    ])
    return InlineKeyboardMarkup(buttons)
