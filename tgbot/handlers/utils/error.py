import logging
import traceback
import html

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from dtb.settings import TELEGRAM_LOGS_CHAT_ID
from users.models import TelegramUser


def send_stacktrace_to_tg_chat(update: Update, context: CallbackContext) -> None:
    u = TelegramUser.get_user(update, context)
    logging.error("=====================================================")
    logging.error("Exception while handling an update:", exc_info=context.error)
    logging.error("User data: %s", context.user_data)
    logging.error("Callback query: %s", update.callback_query)
    logging.error("Context args: %s", context.args)
    logging.error("=====================================================")

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    user_message = """
😔 Щось пішло не так.

Ми вже знаємо що, але спробуйте ще раз спочатку /start
"""
    context.bot.send_message(
        chat_id=u.user_id,
        text=user_message,
    )

    admin_message = f"⚠️⚠️⚠️ for {u.tg_str}:\n{message}"[:4090]
    if TELEGRAM_LOGS_CHAT_ID:
        context.bot.send_message(
            chat_id=TELEGRAM_LOGS_CHAT_ID,
            text=admin_message,
            parse_mode=telegram.ParseMode.HTML,
        )
