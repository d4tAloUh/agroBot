from telegram import Update, Message
from telegram.ext import CallbackContext

from sales.models import SalePlacement
from tgbot.handlers.sale_creation.create_sale.handlers import callback_create_sales_preview
from tgbot.handlers.sale_creation.price.handlers import callback_price_input
from tgbot.handlers.sale_creation.price_type.keyboards import make_choose_price_type_keyboard
from tgbot.handlers.sale_creation.vat.handlers import callback_vat_choosing
from tgbot.handlers.utils.helpers import extract_string, delete_inline_keyboard_on_previous_inline_message

from tgbot.handlers.sale_creation.price_type import static_text


def callback_price_type_chosen(update: Update, context: CallbackContext) -> None:
    price_type_string = extract_string(update.callback_query.data)
    context.user_data["price_type"] = price_type_string
    # Call next step
    if price_type_string == SalePlacement.PriceTypeChoice.F1.value:
        callback_vat_choosing(update, context)
    else:
        callback_price_input(update, context)


def callback_price_type_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.PRICE_TYPE_STEP_NAME

    keyboard = make_choose_price_type_keyboard(
        SalePlacement.PriceTypeChoice
    )
    if update.callback_query:
        update.callback_query.edit_message_text(
            static_text.choose_price_type_text,
            reply_markup=keyboard
        )
    elif update.message:
        # Coming from previous input step
        message: Message = context.bot.send_message(
            update.effective_chat.id,
            static_text.choose_price_type_text,
            reply_markup=keyboard
        )
        delete_inline_keyboard_on_previous_inline_message(
            update, context
        )
        context.user_data["last_message_with_inline"] = message.message_id
