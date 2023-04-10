from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding import static_text


def make_keyboard_for_successful_link_start_command() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(static_text.create_new_sale_text,
                             url="https://github.com/ohld/django-telegram-bot"),
    ]]

    return InlineKeyboardMarkup(buttons)
