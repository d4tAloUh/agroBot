from telegram import Update, Message
from telegram.ext import CallbackContext

from sales.models import SalePlacement
from tgbot.handlers.sale_creation.price.handlers import callback_price_input
from tgbot.handlers.sale_creation.vat.keyboards import make_choose_vat_keyboard
from tgbot.handlers.utils.helpers import extract_string, delete_inline_keyboard_on_previous_inline_message

from tgbot.handlers.sale_creation.vat import static_text


def callback_vat_chosen(update: Update, context: CallbackContext) -> None:
    vat = extract_string(update.callback_query.data)
    # Save selected product id
    context.user_data["vat"] = vat
    # Call next step
    callback_price_input(update, context)


def callback_vat_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.VAT_TYPE_STEP_NAME

    keyboard = make_choose_vat_keyboard(
        SalePlacement.VATChoice
    )
    if update.callback_query:
        update.callback_query.edit_message_text(
            static_text.choose_vat_type_text,
            reply_markup=keyboard
        )
    elif update.message:
        # Coming from previous input step
        message: Message = context.bot.send_message(
            update.effective_chat.id,
            static_text.choose_vat_type_text,
            reply_markup=keyboard
        )
        delete_inline_keyboard_on_previous_inline_message(
            update, context
        )
        context.user_data["last_message_with_inline"] = message.message_id
