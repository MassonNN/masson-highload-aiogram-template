from datetime import datetime, timedelta
from logging import Logger

from aiogram import Bot
from aiogram.types import Message
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from ..exc import CannotPerfromRetry
from ..tkq import broker, schedule_source


@broker.task(retry_on_error=True)
@inject(patch_module=True)
async def pin_message(
    chat_id: int,
    message_id: int,
    bot: FromDishka[Bot],
    logger: FromDishka[Logger],
    notify: bool = False,
    pin: bool = True,
):
    try:
        if pin:
            await bot.pin_chat_message(
                chat_id=chat_id, message_id=message_id, disable_notification=not notify
            )
        else:
            await bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
    except CannotPerfromRetry as cpr:
        logger.warning(
            "Cannot perform retry on pin message",
            cpr=str(cpr),
            message_id=message_id,
            chat_id=chat_id,
        )


async def pin_for_time(message: Message, delta: timedelta, notify: bool = False):
    await pin_message.kiq(
        chat_id=message.chat.id, message_id=message.message_id, notify=notify, pin=True
    )
    await pin_message.schedule_by_time(
        source=schedule_source,
        time=datetime.now() + delta,
        pin=False,
        chat_id=message.chat.id,
        message_id=message.message_id,
    )