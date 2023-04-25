import telegram
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import SalePlacement
from tgbot.handlers.sale_detail.keyboards import make_sale_detail_keyboard, make_delete_sale_confirmation_keyboard, \
    make_deleted_sale_detail_keyboard
from tgbot.handlers.sale_list.utils import get_choose_sale_callback_data
from tgbot.handlers.utils.helpers import extract_id


def callback_sale_delete_confirm(update: Update, context: CallbackContext) -> None:
    from tgbot.handlers.sale_list.handlers import callback_sales_choosing
    sale_id = extract_id(update.callback_query.data)
    sales_page = context.user_data.get("sales_page", 1)
    if not sale_id:
        update.callback_query.data = get_choose_sale_callback_data(sales_page)
        callback_sales_choosing(update, context)
        return
    # Save selected product id
    sale = SalePlacement.objects.filter(
        company__tg_user_id=update.effective_chat.id,
        status=SalePlacement.StatusChoice.POSTED.value,
        id=sale_id
    ).select_related(
        'product', 'company', 'region', 'subregion', 'city'
    ).first()
    if not sale:
        update.callback_query.data = get_choose_sale_callback_data(sales_page)
        callback_sales_choosing(update, context)
        return

    keyboard = make_deleted_sale_detail_keyboard(sales_page=sales_page)

    message_text = sale.generate_sale_inactive_text()
    sale.broadcast_sale_removal(text=message_text)
    sale.status = sale.StatusChoice.DELETED.value
    sale.save()
    update.callback_query.edit_message_text(
        message_text,
        reply_markup=keyboard,
        parse_mode=telegram.ParseMode.HTML
    )


def callback_sale_delete(update: Update, context: CallbackContext) -> None:
    from tgbot.handlers.sale_list.handlers import callback_sales_choosing
    sale_id = extract_id(update.callback_query.data)
    sales_page = context.user_data.get("sales_page", 1)
    if not sale_id:
        update.callback_query.data = get_choose_sale_callback_data(sales_page)
        callback_sales_choosing(update, context)
        return
    sale = SalePlacement.objects.filter(
        company__tg_user_id=update.effective_chat.id,
        status=SalePlacement.StatusChoice.POSTED.value,
        id=sale_id
    ).select_related(
        'product', 'company', 'region', 'subregion', 'city'
    ).first()
    if not sale:
        update.callback_query.data = get_choose_sale_callback_data(sales_page)
        callback_sales_choosing(update, context)
        return
    keyboard = make_delete_sale_confirmation_keyboard(sale_id=sale_id)
    message_text = sale.generate_sale_delete_confirmation_text()
    update.callback_query.edit_message_text(
        message_text,
        reply_markup=keyboard,
        parse_mode=telegram.ParseMode.HTML
    )


def callback_sale_detail(update: Update, context: CallbackContext) -> None:
    from tgbot.handlers.sale_list.handlers import callback_sales_choosing
    sale_id = context.user_data.get("selected_sale")
    sales_page = context.user_data.get("sales_page", 1)
    if not sale_id:
        update.callback_query.data = get_choose_sale_callback_data(sales_page)
        callback_sales_choosing(update, context)
        return
    sale = SalePlacement.objects.filter(
        company__tg_user_id=update.effective_chat.id,
        status=SalePlacement.StatusChoice.POSTED.value,
        id=sale_id
    ).select_related(
        'product', 'company', 'region', 'subregion', 'city'
    ).first()
    if not sale:
        update.callback_query.data = get_choose_sale_callback_data(sales_page)
        callback_sales_choosing(update, context)
        return
    keyboard = make_sale_detail_keyboard(sale_id=sale_id, sales_page=sales_page)
    message_text = sale.generate_sale_text()
    update.callback_query.edit_message_text(
        message_text,
        reply_markup=keyboard,
        parse_mode=telegram.ParseMode.HTML
    )
