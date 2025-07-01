"""This file is example of delayed answer implementation with taskiq."""
from datetime import timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.worker.tasks.send_message import delay_send_message

delayed_answer_router = Router()


@delayed_answer_router.message(Command('answerme'))
async def delayed_answer(message: Message):
    await delay_send_message(
        chat_id=message.from_user.id,
        text="This answer was sent with a delay of 1 minute.",
        delta=timedelta(minutes=1)
    )
