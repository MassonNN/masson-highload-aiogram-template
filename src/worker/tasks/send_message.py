from datetime import datetime, timedelta
from logging import Logger

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from ..tkq import broker, schedule_source
from ..exc import CannotPerfromRetry


@broker.task(retry_on_error=True)
@inject(patch_module=True)
async def send_message(
        chat_id: int,
        text: str,
        bot: FromDishka[Bot],
        logger: FromDishka[Logger],
):
    try:
        await bot.send_message(
            chat_id=chat_id, text=text
        )
    except CannotPerfromRetry as cpr:
        logger.warning(
            "Cannot perform retry on send message",
            cpr=str(cpr),
            chat_id=chat_id,
            text=text,
        )


async def delay_send_message(chat_id: int, text: str, delta: timedelta):
    await send_message.schedule_by_time(
        source=schedule_source,
        time=datetime.now() + delta,
        chat_id=chat_id,
        text=text
    )
