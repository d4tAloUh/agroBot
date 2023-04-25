"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time
from typing import Union, List, Optional, Dict

import telegram

from dtb.celery import app
from celery.utils.log import get_task_logger

from sales.utils import from_celery_markup_to_markup, send_one_message
from dtb.settings import TELEGRAM_TOKEN

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def broadcast_sale_message(
    sale_id:str,
    user_ids: List[Union[str, int]],
    text: str,
    reply_markup: Optional[List[List[Dict]]] = None,
    sleep_between: float = 0.4,
    parse_mode=telegram.ParseMode.HTML,
) -> None:
    from sales.models import SentSaleMessage
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{text}' to {len(user_ids)} users")
    # TODO: add retry handler
    reply_markup_ = from_celery_markup_to_markup(reply_markup)
    sent_messages = []
    for user_id in user_ids:
        try:
            success, message = send_one_message(
                user_id=user_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup_,
            )
            if success:
                sent_messages.append(SentSaleMessage(
                    message_id=message.message_id,
                    chat_id=user_id,
                    sale_id=sale_id
                ))
                logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}")
        time.sleep(max(sleep_between, 0.1))
    if sent_messages:
        SentSaleMessage.objects.bulk_create(sent_messages)
        logger.info(f"Saved sale '{sale_id}' messages: {len(sent_messages)}")
    logger.info(f"Broadcast '{sale_id}' sale finished!")


@app.task(ignore_result=True)
def broadcast_edit_message(
    sale_id: str,
    user_with_messages_ids,
    text: str,
    sleep_between: float = 0.4,
    parse_mode=telegram.ParseMode.HTML,
) -> None:
    """ It's used to edit a lot of messages """
    logger.info(f"Going to set inactive sale '{sale_id}'")
    # TODO: add retry handler
    bot = telegram.Bot(TELEGRAM_TOKEN)
    for user_id, message_id in user_with_messages_ids:
        try:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=text,
                parse_mode=parse_mode,
            )
            logger.info(f"Sale '{sale_id}' was set inactive for {user_id}")
        except telegram.error.Unauthorized:
            print(f"Can't send message to {user_id}. Reason: Bot was stopped.")
        except Exception as e:
            logger.error(f"Failed to edit message {user_id} with id '{message_id}', reason: {e}")
        time.sleep(max(sleep_between, 0.1))

    logger.info(f"Broadcast '{sale_id}' inactive finished!")
