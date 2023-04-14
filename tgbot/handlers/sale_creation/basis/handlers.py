from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.sale_creation.basis import static_text
from tgbot.handlers.sale_creation.basis.keyboards import make_select_basis_keyboard


def callback_basis_input(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.BASIS_STEP_NAME

    # Coming from previous step or next
    if update.callback_query:
        keyboard = make_select_basis_keyboard()
        update.callback_query.edit_message_text(
            static_text.input_basis_text,
            reply_markup=keyboard
        )
    elif update.message:
        # User answered
        context.user_data["basis"] = update.message.text
        context.bot.send_message(
            update.effective_chat.id,
            "VSYO"
        )
