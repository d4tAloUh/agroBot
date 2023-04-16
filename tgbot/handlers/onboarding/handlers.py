from telegram import Update
from telegram.ext import CallbackContext

from sales.models import CompanyAccount
from tgbot.handlers.menu.keyboards import make_menu_keyboard
from tgbot.handlers.onboarding import static_text
from users.models import TelegramUser


def command_start(update: Update, context: CallbackContext) -> None:
    u = TelegramUser.get_user(update, context)

    keyboard = None
    text = None
    if context.args and len(context.args) == 1:
        invite_code = context.args[0]
        company_account = CompanyAccount.objects.filter(
            invite_code=invite_code,
            tg_user__isnull=True
        ).first()
        if company_account:
            company_account.tg_user = u
            company_account.save()
            text = static_text.successfully_linked.format(account_name=company_account.name)
            keyboard = make_menu_keyboard()
    if text is None:
        if u.is_registered:
            text = static_text.greeting_text
            keyboard = make_menu_keyboard()
        else:
            text = static_text.unregistered_text

    update.message.reply_text(text=text, reply_markup=keyboard)
