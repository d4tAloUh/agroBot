from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.menu import static_text
from tgbot.handlers.menu.keyboards import make_menu_keyboard


def callback_menu(update: Update, context: CallbackContext) -> None:
    keyboard = make_menu_keyboard()
    update.callback_query.edit_message_text(
        static_text.menu_text,
        reply_markup=keyboard
    )
