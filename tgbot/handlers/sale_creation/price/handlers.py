from telegram import Update, Message
from telegram.ext import CallbackContext

from tgbot.handlers.sale_creation.basis.static_text import BASIS_STEP_NAME
from tgbot.handlers.sale_creation.create_sale.handlers import callback_create_sales_preview
from tgbot.handlers.sale_creation.price import static_text
from tgbot.handlers.sale_creation.price.keyboards import make_input_price_keyboard
from tgbot.handlers.utils.helpers import delete_inline_keyboard_on_previous_inline_message


def callback_price_input(update: Update, context: CallbackContext) -> None:
    keyboard = make_input_price_keyboard()
    # Coming from previous step or next
    if update.callback_query:
        context.user_data["current_step"] = static_text.PRICE_STEP_NAME
        update.callback_query.edit_message_text(
            static_text.input_price_text,
            reply_markup=keyboard
        )
    elif update.message and context.user_data.get("current_step") == BASIS_STEP_NAME:
        context.user_data["current_step"] = static_text.PRICE_STEP_NAME
        # Coming from previous input step
        message: Message = context.bot.send_message(
            update.effective_chat.id,
            static_text.input_price_text,
            reply_markup=keyboard
        )
        delete_inline_keyboard_on_previous_inline_message(
            update, context
        )
        context.user_data["last_message_with_inline"] = message.message_id
    elif update.message:
        # User answered
        context.user_data["price"] = update.message.text
        callback_create_sales_preview(update, context)
