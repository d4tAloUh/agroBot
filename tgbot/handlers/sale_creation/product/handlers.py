from django.core.paginator import Paginator
from django.db.models import Value
from telegram import Update
from telegram.ext import CallbackContext

from sales.models import Product, ProductType
from tgbot.handlers.sale_creation.product.utils import get_product_chosen_callback_data, \
    get_choose_product_callback_data, get_go_back_from_choose_product_callback_data, \
    get_go_back_from_product_type_callback_data
from tgbot.handlers.sale_creation.weight.handlers import callback_weight_input
from tgbot.handlers.utils.helpers import extract_page, extract_id, clear_user_data_for_sale, extract_second_parameter

from tgbot.handlers.sale_creation.product import static_text
from tgbot.handlers.utils.keyboards import make_paginated_keyboard


def callback_go_back_from_product_type(update: Update, context: CallbackContext) -> None:
    if "product_type" in context.user_data:
        del context.user_data["product_type"]
    update.callback_query.data = get_choose_product_callback_data(1)
    callback_product_choosing(update, context)


def callback_product_chosen(update: Update, context: CallbackContext) -> None:
    entity_id = extract_id(update.callback_query.data)
    is_product = extract_second_parameter(update.callback_query.data)
    if is_product == 'True':
        # Save selected product id
        context.user_data["product_id"] = entity_id
        # Call next step
        callback_weight_input(update, context)
    else:
        # Save selected product id
        context.user_data["product_type"] = entity_id

        # Call next step
        update.callback_query.data = get_choose_product_callback_data(1)
        callback_product_choosing(update, context)


def callback_product_choosing(update: Update, context: CallbackContext) -> None:
    context.user_data["current_step"] = static_text.PRODUCT_STEP_NAME
    product_type_id = context.user_data.get("product_type")
    if not product_type_id:
        products = Product.objects.filter(
            product_type__isnull=True
        ).annotate(
            is_product=Value(True)
        ).values("pk", "name", "order", "is_product")
        product_type = ProductType.objects.annotate(
            is_product=Value(False)
        ).values("pk", "name", "order", "is_product")
        results = product_type.union(products).order_by("is_product", "order")
        go_back_text = static_text.go_back_text
        go_back_callback = get_go_back_from_choose_product_callback_data()
    else:
        results = Product.objects.filter(
            product_type_id=product_type_id
        ).annotate(
            is_product=Value(True)
        ).values("pk", "name", "order", "is_product").order_by("order")
        go_back_text = static_text.go_back_from_product_type_text
        go_back_callback = get_go_back_from_product_type_callback_data()
    page = extract_page(update.callback_query.data)
    paginator = Paginator(
        object_list=results,
        per_page=static_text.products_per_row * static_text.product_rows
    )
    products_page = paginator.get_page(page)
    keyboard = make_paginated_keyboard(
        items = products_page.object_list,
        page=page,
        item_text_getter=lambda x:x["name"],
        is_last_page=not products_page.has_next(),
        get_item_callback=get_product_chosen_callback_data,
        prev_page_callback=get_choose_product_callback_data(page - 1),
        next_page_callback=get_choose_product_callback_data(page + 1),
        go_back_callback=go_back_callback,
        go_back_text=go_back_text,
        rows=static_text.product_rows,
        per_row=static_text.products_per_row
    )
    update.callback_query.edit_message_text(
        static_text.choose_product_text,
        reply_markup=keyboard
    )
