from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from sales.models import SalePlacement, CompanyAccount
from tgbot.handlers.menu.handlers import callback_menu
from tgbot.handlers.sale_creation.create_sale.keyboards import make_sales_preview_keyboard, create_new_sale_keyboard
from tgbot.handlers.sale_creation.create_sale import static_text


def callback_confirm_sale_creation(update: Update, context: CallbackContext) -> None:
    sale = SalePlacement.create_unsaved_sale_from_user_data(
        update.effective_chat.id,
        context.user_data
    )
    sale.save()
    sale_text = sale.generate_sale_text()
    # Send sale
    update.callback_query.edit_message_text(
        sale_text,
        parse_mode=ParseMode.HTML
    )
    # Force to send message
    update.callback_query = None
    callback_menu(update, context)


def callback_create_sales_preview(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.SALE_PREVIEW_STEP
    keyboard = make_sales_preview_keyboard()
    sale = SalePlacement.create_unsaved_sale_from_user_data(
        update.effective_chat.id,
        context.user_data
    )
    sale_text = sale.generate_sale_preview_text()
    context.bot.send_message(
        update.effective_chat.id,
        sale_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

