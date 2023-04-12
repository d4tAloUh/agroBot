from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.sale_creation.region.handlers import callback_region_choosing
from tgbot.handlers.sale_creation.weight import static_text
from tgbot.handlers.sale_creation.weight.keyboards import make_select_weight_keyboard


def callback_weight_input(update: Update, context: CallbackContext) -> None:
    print("Callback query in weight:", update.callback_query)
    context.user_data["current_step"] = static_text.WEIGHT_STEP_NAME

    # Coming from previous step or next
    if update.callback_query:
        keyboard = make_select_weight_keyboard()
        update.callback_query.edit_message_text(
            static_text.input_weight_text,
            reply_markup=keyboard
        )
    elif update.message:
        # User answered
        context.user_data["weight"] = update.message.text
        callback_region_choosing(update, context)
