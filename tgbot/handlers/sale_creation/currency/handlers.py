from telegram import Update, Message
from telegram.ext import CallbackContext

from sales.models import SalePlacement
from tgbot.handlers.sale_creation.currency.keyboards import make_choose_currency_keyboard
from tgbot.handlers.sale_creation.price_type.handlers import callback_price_type_choosing
from tgbot.handlers.utils.helpers import extract_string

from tgbot.handlers.sale_creation.currency import static_text


def callback_currency_chosen(update: Update, context: CallbackContext) -> None:
    currency = extract_string(update.callback_query.data)
    # Save selected product id
    context.user_data["currency"] = currency
    # Call next step
    callback_price_type_choosing(update, context)


def callback_currency_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.CURRENCY_STEP_NAME

    keyboard = make_choose_currency_keyboard(
        SalePlacement.CurrencyChoice
    )
    if update.callback_query:
        update.callback_query.edit_message_text(
            static_text.choose_currency_text,
            reply_markup=keyboard
        )
    elif update.message:
        # Coming from previous input step
        message: Message = context.bot.send_message(
            update.effective_chat.id,
            static_text.choose_currency_text,
            reply_markup=keyboard
        )
        context.user_data["last_message_with_inline"] = message.message_id
