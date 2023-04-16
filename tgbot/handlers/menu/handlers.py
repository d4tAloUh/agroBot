from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.menu.keyboards import make_menu_keyboard
from tgbot.handlers.onboarding.static_text import greeting_text


def callback_menu(update: Update, context: CallbackContext) -> None:
    keyboard = make_menu_keyboard()
    update.callback_query.edit_message_text(
        greeting_text,
        reply_markup=keyboard
    )
