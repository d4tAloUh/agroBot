from __future__ import annotations

from typing import Tuple

from django.db import models
from django.db.models import QuerySet, Manager
from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.utils.info import extract_user_data_from_update
from utils.models import CreateUpdateTracker, nb, CreateTracker, GetOrNoneManager


class AdminTelegramUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class TelegramUser(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(verbose_name="Chat ID", primary_key=True)  # telegram_id
    username = models.CharField(verbose_name="Username", max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)

    is_admin = models.BooleanField(default=False)

    objects = GetOrNoneManager()
    admins = AdminTelegramUserManager()

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_or_create(cls, update: Update, context: CallbackContext) -> Tuple[TelegramUser, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)
        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> TelegramUser:
        u, _ = cls.get_user_or_create(update, context)
        return u

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"

    @property
    def is_registered(self) -> bool:
        return hasattr(self, "company_account")

