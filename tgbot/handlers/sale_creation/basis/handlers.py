from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.sale_creation.basis import static_text
from tgbot.handlers.sale_creation.basis.keyboards import make_select_basis_keyboard
from tgbot.handlers.sale_creation.basis.utils import get_go_back_from_basis_callback_data
from tgbot.handlers.sale_creation.currency.handlers import callback_currency_choosing
from tgbot.handlers.utils.helpers import extract_string


def callback_basis_chosen(update: Update, context: CallbackContext) -> None:
    basis = extract_string(update.callback_query.data)
    context.user_data["basis"] = basis
    # Call next step
    callback_currency_choosing(update, context)


def callback_basis_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.BASIS_STEP_NAME

    # Coming from previous step or next
    callback_data, text = get_go_back_from_basis_callback_data(context)
    keyboard = make_select_basis_keyboard(callback_data=callback_data, text=text)
    update.callback_query.edit_message_text(
        static_text.input_basis_text,
        reply_markup=keyboard
    )
