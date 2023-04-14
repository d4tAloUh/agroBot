from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.sale_creation.price import static_text
from tgbot.handlers.sale_creation.price.keyboards import make_input_price_keyboard


def callback_price_input(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.PRICE_STEP_NAME

    # Coming from previous step or next
    if update.callback_query:
        keyboard = make_input_price_keyboard()
        update.callback_query.edit_message_text(
            static_text.input_price_text,
            reply_markup=keyboard
        )
    elif update.message:
        # User answered
        context.user_data["price"] = update.message.text
        context.bot.send_message(
            update.effective_chat.id,
            "VSYO"
        )
