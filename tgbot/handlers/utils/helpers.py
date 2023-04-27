from typing import Dict

from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.utils import static_text


def extract_page(callback_text: str) -> int:
    """
        Page should be first parameter after callback text
    """
    split_text = callback_text.split(static_text.callback_separator)
    return int(split_text[1])


extract_id = extract_page


def extract_string(callback_text: str) -> str:
    """
        string should be first parameter after callback text
    """
    split_text = callback_text.split(static_text.callback_separator)
    return split_text[1]


def extract_is_city(callback_text: str) -> str:
    """
        is_city should be second parameter after callback text
    """
    split_text = callback_text.split(static_text.callback_separator)
    return split_text[2]


def extract_id_with_value(callback_text:str):
    """
        id should be second parameter after callback text
        value should be third
    """
    split_text = callback_text.split(static_text.callback_separator)
    selected_id = None
    selected_value = None
    if len(split_text) > 2:
        selected_id = int(split_text[2])
        selected_value = split_text[3] == 'True'
    return selected_id, selected_value


def delete_inline_keyboard_on_previous_inline_message(update: Update, context: CallbackContext):
    message_id = context.user_data.get("last_message_with_inline")
    if not message_id:
        return
    try:
        context.bot.edit_message_reply_markup(
            update.effective_chat.id,
            message_id=message_id,
            reply_markup=None
        )
    except Exception:
        pass


