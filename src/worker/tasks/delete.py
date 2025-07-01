import datetime
from collections.abc import Collection
from logging import Logger

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from ..exc import CannotPerfromRetry
from ..tkq import broker, schedule_source


@broker.task(retry_on_error=True)
@inject(patch_module=True)
async def delete_message_task(
    chat_id: int,
    message_id: int,
    bot: FromDishka[Bot],
    logger: FromDishka[Logger],
):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except CannotPerfromRetry as cpr:
        logger.warning(
            "Cannot perform retry on delete message",
            exc=str(cpr),
            message_id=message_id,
            chat_id=chat_id,
        )


async def _delete_message(
    chat_id: int,
    message_id: int,
    delay: datetime.timedelta = None,
):
    if delay:
        return await delete_message_task.schedule_by_time(
            source=schedule_source,
            time=datetime.datetime.now() + delay,
            chat_id=chat_id,
            message_id=message_id,
        )
    else:
        return await delete_message_task.kiq(chat_id=chat_id, message_id=message_id)


async def delete_message(
    chat_id: int,
    message_id: int,
    delay: int | datetime.timedelta | datetime.datetime = None,
):
    if not delay:
        return await _delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )
    if isinstance(delay, int):
        return await _delete_message(
            chat_id=chat_id,
            message_id=message_id,
            delay=datetime.timedelta(seconds=delay),
        )
    elif isinstance(delay, datetime.timedelta):
        return await _delete_message(
            chat_id=chat_id,
            message_id=message_id,
            delay=delay,
        )
    elif isinstance(delay, datetime.datetime):
        return await _delete_message(
            chat_id=chat_id,
            message_id=message_id,
            delay=delay - datetime.datetime.now(),
        )

    else:
        raise ValueError(
            f"Delay is not a valid type (int, datetime, timedelta), its type: {type(delay)}"
        )


async def delete_messages_tg(
    *messages, delay: int | datetime.timedelta | datetime.datetime | None = None
):
    for message in messages:
        await delete_message(
            chat_id=message.chat.id, message_id=message.message_id, delay=delay
        )
