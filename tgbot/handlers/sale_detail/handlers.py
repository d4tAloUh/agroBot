from telegram import Update
from telegram.ext import CallbackContext

from sales.models import SalePlacement
from tgbot.handlers.sale_detail.keyboards import make_sale_detail_keyboard
from tgbot.handlers.utils.helpers import extract_id


def callback_sale_delete(update: Update, context: CallbackContext) -> None:
    sale_id = extract_id(update.callback_query.data)
    # Save selected product id
    print("Sale id to delete:", sale_id)


def callback_sale_detail(update: Update, context: CallbackContext) -> None:
    from tgbot.handlers.sales.handlers import callback_sales_choosing
    sale_id = context.user_data.get("selected_sale")
    if not sale_id:
        callback_sales_choosing(update, context)
    sale = SalePlacement.objects.filter(
        company__tg_user_id=update.effective_chat.id,
        status=SalePlacement.StatusChoice.POSTED.value,
        id=sale_id
    ).select_related('product').first()
    if not sale:
        callback_sales_choosing(update, context)
    keyboard = make_sale_detail_keyboard(sale_id=sale_id)
    message_text = sale.generate_sale_text()
    update.callback_query.edit_message_text(
        message_text,
        reply_markup=keyboard
    )
