from telegram import Update, Message
from telegram.ext import CallbackContext

from tgbot.handlers.menu.keyboards import make_menu_keyboard
from tgbot.handlers.onboarding.static_text import greeting_text
from tgbot.handlers.utils.helpers import delete_inline_keyboard_on_previous_inline_message


def callback_menu(update: Update, context: CallbackContext) -> None:
    keyboard = make_menu_keyboard()
    if update.callback_query:
        update.callback_query.edit_message_text(
            greeting_text,
            reply_markup=keyboard
        )
    else:
        message: Message = context.bot.send_message(
            update.effective_chat.id,
            greeting_text,
            reply_markup=keyboard
        )
        delete_inline_keyboard_on_previous_inline_message(
            update, context
        )
        context.user_data["last_message_with_inline"] = message.message_id
