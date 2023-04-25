"""
    Telegram event handlers
"""
from telegram import Update
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    CallbackQueryHandler, TypeHandler,
    CallbackContext, DispatcherHandlerStop,
)

from dtb.settings import DEBUG
from tgbot.handlers.sale_buying.manage_data import CHOOSE_PRODUCT_INTEREST_CALLBACK, PRODUCT_INTEREST_CHOSEN_CALLBACK
from tgbot.handlers.sale_creation.basis.manage_data import INPUT_BASIS_CALLBACK
from tgbot.handlers.sale_creation.basis.static_text import BASIS_STEP_NAME
from tgbot.handlers.sale_creation.city.manage_data import CHOOSE_CITY_CALLBACK, CITY_CHOSEN_CALLBACK
from tgbot.handlers.sale_creation.create_sale.manage_data import ACCEPT_SALE_CALLBACK
from tgbot.handlers.sale_creation.currency.manage_data import CHOOSE_CURRENCY_CALLBACK, CHOSEN_CURRENCY_CALLBACK
from tgbot.handlers.sale_creation.price.manage_data import INPUT_PRICE_CALLBACK
from tgbot.handlers.sale_creation.price.static_text import PRICE_STEP_NAME
from tgbot.handlers.sale_creation.price_type.manage_data import CHOOSE_PRICE_TYPE_CALLBACK, CHOSEN_PRICE_TYPE_CALLBACK
from tgbot.handlers.sale_creation.region.manage_data import REGION_CHOSEN_CALLBACK, CHOOSE_REGION_CALLBACK
from tgbot.handlers.sale_creation.subregion.manage_data import SUBREGION_CHOSEN_CALLBACK, CHOOSE_SUBREGION_CALLBACK
from tgbot.handlers.sale_creation.vat.manage_data import CHOOSE_VAT_CALLBACK, CHOSEN_VAT_CALLBACK
from tgbot.handlers.sale_creation.weight.manage_data import INPUT_WEIGHT_CALLBACK
from tgbot.handlers.sale_creation.weight.static_text import WEIGHT_STEP_NAME
from tgbot.handlers.sale_detail.manage_data import DELETE_SALE_CALLBACK, CONFIRM_DELETE_SALE_CALLBACK
from tgbot.handlers.sale_list.manage_data import CHOOSE_SALE_CALLBACK, SALE_CHOSEN_CALLBACK

from tgbot.handlers.utils import error
from tgbot.handlers.onboarding import handlers as onboarding_handlers

from tgbot.handlers.sale_creation.product import handlers as product_choosing_sales_handler
from tgbot.handlers.sale_creation.product.manage_data import CHOOSE_PRODUCT_CALLBACK, PRODUCT_CHOSEN_CALLBACK

from tgbot.handlers.menu.manage_data import MENU_CALLBACK_DATA
from tgbot.handlers.menu import handlers as menu_handlers

from tgbot.handlers.sale_creation.weight import handlers as weight_handlers
from tgbot.handlers.sale_creation.region import handlers as region_handlers
from tgbot.handlers.sale_creation.subregion import handlers as subregion_handlers
from tgbot.handlers.sale_creation.city import handlers as cities_handlers
from tgbot.handlers.sale_creation.basis import handlers as basis_handlers
from tgbot.handlers.sale_creation.price import handlers as price_handlers
from tgbot.handlers.sale_creation.currency import handlers as currency_handlers
from tgbot.handlers.sale_creation.price_type import handlers as price_type_handlers
from tgbot.handlers.sale_creation.vat import handlers as vat_handlers
from tgbot.handlers.sale_creation.create_sale import handlers as sale_creation_handlers
from tgbot.handlers.sale_list import handlers as sales_handlers
from tgbot.handlers.sale_detail import handlers as sale_detail_handlers
from tgbot.handlers.sale_buying import handlers as sale_buying_handlers
from tgbot.handlers.utils.static_text import callback_separator

from tgbot.main import bot


def setup_type_handler(update: Update, context: CallbackContext) -> None:
    # print("user data:", context.user_data)
    # print("Update query", update.callback_query)
    if update.message:
        if context.user_data.get("current_step", None) == WEIGHT_STEP_NAME:
            weight_handlers.callback_weight_input(update, context)
            raise DispatcherHandlerStop
        if context.user_data.get("current_step", None) == BASIS_STEP_NAME:
            basis_handlers.callback_basis_input(update, context)
            raise DispatcherHandlerStop
        if context.user_data.get("current_step", None) == PRICE_STEP_NAME:
            price_handlers.callback_price_input(update, context)
            raise DispatcherHandlerStop


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    dp.add_handler(TypeHandler(Update, setup_type_handler), -1)
    # onboarding
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))

    # Handle menu callback
    dp.add_handler(
        CallbackQueryHandler(menu_handlers.callback_menu,
                             pattern=f"^{MENU_CALLBACK_DATA}$")
    )
    # Handle product selection
    dp.add_handler(
        CallbackQueryHandler(product_choosing_sales_handler.callback_product_choosing,
                             pattern=f"^{CHOOSE_PRODUCT_CALLBACK}{callback_separator}")
    )
    dp.add_handler(
        CallbackQueryHandler(product_choosing_sales_handler.callback_product_chosen,
                             pattern=f"^{PRODUCT_CHOSEN_CALLBACK}{callback_separator}")
    )
    # Handle weight input in TypeHandler
    # Handle weight go back callback
    dp.add_handler(
        CallbackQueryHandler(weight_handlers.callback_weight_input,
                             pattern=f"^{INPUT_WEIGHT_CALLBACK}")
    )
    # Handle region selection
    dp.add_handler(
        CallbackQueryHandler(region_handlers.callback_region_choosing,
                             pattern=f"^{CHOOSE_REGION_CALLBACK}")
    )
    dp.add_handler(
        CallbackQueryHandler(region_handlers.callback_region_chosen,
                             pattern=f"^{REGION_CHOSEN_CALLBACK}")
    )

    # Handle subregion selection
    dp.add_handler(
        CallbackQueryHandler(subregion_handlers.callback_subregion_choosing,
                             pattern=f"^{CHOOSE_SUBREGION_CALLBACK}")
    )
    dp.add_handler(
        CallbackQueryHandler(subregion_handlers.callback_subregion_chosen,
                             pattern=f"^{SUBREGION_CHOSEN_CALLBACK}")
    )

    # Handle city selection
    dp.add_handler(
        CallbackQueryHandler(cities_handlers.callback_city_choosing,
                             pattern=f"^{CHOOSE_CITY_CALLBACK}")
    )
    dp.add_handler(
        CallbackQueryHandler(cities_handlers.callback_city_chosen,
                             pattern=f"^{CITY_CHOSEN_CALLBACK}")
    )

    # Handle go back to basis callback
    dp.add_handler(
        CallbackQueryHandler(basis_handlers.callback_basis_input,
                             pattern=f"^{INPUT_BASIS_CALLBACK}")
    )

    # Handle go back to price callback
    dp.add_handler(
        CallbackQueryHandler(price_handlers.callback_price_input,
                             pattern=f"^{INPUT_PRICE_CALLBACK}")
    )

    # Handle currency selection
    dp.add_handler(
        CallbackQueryHandler(currency_handlers.callback_currency_choosing,
                             pattern=f"^{CHOOSE_CURRENCY_CALLBACK}")
    )
    dp.add_handler(
        CallbackQueryHandler(currency_handlers.callback_currency_chosen,
                             pattern=f"^{CHOSEN_CURRENCY_CALLBACK}")
    )

    # Handle price_type selection
    dp.add_handler(
        CallbackQueryHandler(price_type_handlers.callback_price_type_choosing,
                             pattern=f"^{CHOOSE_PRICE_TYPE_CALLBACK}")
    )
    dp.add_handler(
        CallbackQueryHandler(price_type_handlers.callback_price_type_chosen,
                             pattern=f"^{CHOSEN_PRICE_TYPE_CALLBACK}")
    )

    # Handle vat selection
    dp.add_handler(
        CallbackQueryHandler(vat_handlers.callback_vat_choosing,
                             pattern=f"^{CHOOSE_VAT_CALLBACK}")
    )
    dp.add_handler(
        CallbackQueryHandler(vat_handlers.callback_vat_chosen,
                             pattern=f"^{CHOSEN_VAT_CALLBACK}")
    )

    # Handle sale creation confirmation
    dp.add_handler(
        CallbackQueryHandler(sale_creation_handlers.callback_confirm_sale_creation,
                             pattern=f"^{ACCEPT_SALE_CALLBACK}")
    )

    # Handle my sale_list
    dp.add_handler(
        CallbackQueryHandler(sales_handlers.callback_sales_choosing,
                             pattern=f"^{CHOOSE_SALE_CALLBACK}")
    )

    dp.add_handler(
        CallbackQueryHandler(sales_handlers.callback_sale_chosen,
                             pattern=f"^{SALE_CHOSEN_CALLBACK}")
    )
    # handling sale detail
    dp.add_handler(
        CallbackQueryHandler(sale_detail_handlers.callback_sale_delete,
                             pattern=f"^{DELETE_SALE_CALLBACK}")
    )

    dp.add_handler(
        CallbackQueryHandler(sale_detail_handlers.callback_sale_delete_confirm,
                             pattern=f"^{CONFIRM_DELETE_SALE_CALLBACK}")
    )
    # handling product interest (sale buying)
    dp.add_handler(
        CallbackQueryHandler(sale_buying_handlers.callback_product_choosing,
                             pattern=f"^{CHOOSE_PRODUCT_INTEREST_CALLBACK}")
    )
    dp.add_handler(
        CallbackQueryHandler(sale_buying_handlers.callback_product_choosing,
                             pattern=f"^{PRODUCT_INTEREST_CHOSEN_CALLBACK}")
    )

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(
    Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True)
)
