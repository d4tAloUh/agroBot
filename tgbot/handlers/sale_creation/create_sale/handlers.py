from telegram import Update
from telegram.ext import CallbackContext

from sales.models import SalesPlacement
from tgbot.handlers.sale_creation.create_sale.keyboards import make_sales_preview_keyboard
from tgbot.handlers.sale_creation.create_sale import static_text


def callback_create_sales_preview(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.SALE_PREVIEW_STEP
    keyboard = make_sales_preview_keyboard()
    sale_text = SalesPlacement.generate_sale_preview(context.user_data)
    update.callback_query.edit_message_text(
        static_text.sale_preview_text.format(sale_text=sale_text),
        reply_markup=keyboard
    )

