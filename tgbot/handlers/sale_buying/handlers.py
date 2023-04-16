from django.core.paginator import Paginator
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import Product, ProductInterest, CompanyAccount
from tgbot.handlers.onboarding.handlers import command_start
from tgbot.handlers.sale_buying.utils import get_product_interest_text_function, \
    get_go_back_from_choose_product_interest_callback_data, get_choose_product_interest_callback_data, \
    get_product_interest_chosen_callback_data_function
from tgbot.handlers.utils.helpers import extract_page, extract_id_with_value

from tgbot.handlers.sale_buying import static_text
from tgbot.handlers.utils.keyboards import make_paginated_keyboard


def callback_product_choosing(update: Update, context: CallbackContext) -> None:
    product_id, value = extract_id_with_value(update.callback_query.data)
    if product_id:
        company_account = CompanyAccount.objects.filter(
            tg_user_id=update.effective_chat.id
        ).first()
        if not company_account:
            command_start(update, context)
        if value:
            ProductInterest.objects.update_or_create(
                product_id=product_id,
                company=company_account
            )
        else:
            ProductInterest.objects.filter(
                product_id=product_id,
                company=company_account
            ).delete()

    interests = ProductInterest.objects.filter(
        company__tg_user_id=update.effective_chat.id
    ).values_list('product_id', flat=True)
    products = Product.objects.order_by('order')
    page = extract_page(update.callback_query.data)
    paginator = Paginator(
        object_list=products,
        per_page=static_text.products_per_row * static_text.product_rows
    )
    products_page = paginator.get_page(page)
    keyboard = make_paginated_keyboard(
        items = products_page.object_list,
        page=page,
        item_text_getter=get_product_interest_text_function(interests),
        is_last_page=not products_page.has_next(),
        get_item_callback=get_product_interest_chosen_callback_data_function(page, interests),
        prev_page_callback=get_choose_product_interest_callback_data(page - 1),
        next_page_callback=get_choose_product_interest_callback_data(page + 1),
        go_back_callback=get_go_back_from_choose_product_interest_callback_data(),
        go_back_text=static_text.go_back_text
    )
    update.callback_query.edit_message_text(
        static_text.choose_product_interest_text,
        reply_markup=keyboard
    )
