import json
import logging
from django.views import View
from django.http import JsonResponse
from telegram import Update

from dtb.celery import app
from dtb.settings import DEBUG
from tgbot.dispatcher import dispatcher
from tgbot.main import bot

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def index(request):
    return JsonResponse({"error": "you found this page!!!!"})


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)!
            # Locally, You can run all of these services via docker-compose.yml
            process_telegram_event.delay(json.loads(request.body))

        return JsonResponse({"ok": "1"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "1"})
