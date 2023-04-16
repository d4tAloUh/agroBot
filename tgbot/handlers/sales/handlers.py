from django.core.paginator import Paginator
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import SalesPlacement
from tgbot.handlers.sale_detail.handlers import callback_sale_detail
from tgbot.handlers.sales.utils import get_choose_sale_callback_data, get_go_back_from_choose_sale_callback_data, \
    get_sale_chosen_callback_data, get_sale_button_text
from tgbot.handlers.utils.helpers import extract_page, extract_id

from tgbot.handlers.sales import static_text
from tgbot.handlers.utils.keyboards import make_paginated_keyboard


def callback_sale_chosen(update: Update, context: CallbackContext) -> None:
    sale_id = extract_id(update.callback_query.data)
    # Save selected product id
    context.user_data["selected_sale"] = sale_id
    # Call next step
    callback_sale_detail(update, context)


def callback_sales_choosing(update: Update, context: CallbackContext) -> None:
    sales = SalesPlacement.objects.filter(
        company__tg_user_id=update.effective_chat.id
    ).select_related('product').order_by('created_at')
    page = extract_page(update.callback_query.data)
    paginator = Paginator(
        object_list=sales,
        per_page=static_text.sales_per_row * static_text.sale_rows
    )
    sales_page = paginator.get_page(page)
    keyboard = make_paginated_keyboard(
        items = sales_page.object_list,
        page=page,
        is_last_page=not sales_page.has_next(),
        item_text_getter=get_sale_button_text,
        get_item_callback=get_sale_chosen_callback_data,
        prev_page_callback=get_choose_sale_callback_data(page - 1),
        next_page_callback=get_choose_sale_callback_data(page + 1),
        go_back_callback=get_go_back_from_choose_sale_callback_data(),
        go_back_text=static_text.go_back_text
    )
    update.callback_query.edit_message_text(
        static_text.choose_sale_text,
        reply_markup=keyboard
    )
