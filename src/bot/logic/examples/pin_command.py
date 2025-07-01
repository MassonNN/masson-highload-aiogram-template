"""Example of message pin with unpin delaying."""
import re
from datetime import timedelta

from aiogram import Router, F
from aiogram.types import Message

from src.worker.tasks.delete import delete_messages_tg
from src.worker.tasks.pin import pin_for_time, pin_message


"""
This file is from one of my current highload projects.
Here are you can see my approach to use different routers for different project parts
in action. I can easily add filters or middlewares to pin_router and this will have
effect only for pin command logic. 

I really suggest to make filtering in this way.
Dont forget to include this router (if you want to test it) 
to routers list in src.bot.logic/__init__.py
"""

pin_router = Router()


"""I like to use regular expressions for commands arguments"""
PIN_REGEXP = re.compile(r"/pin(?P<timedelta> \d+[mhdw])?(?P<is_notify> notify)?")


def timedelta_generator(timedelta_str: str) -> timedelta | None:
    """
    This function transfers timedelta string in human-readable format to timedelta object.

    Example: 3h -> timedelta(hours=3)
    """
    multiplicator = timedelta_str[-1:]
    try:
        value = int(timedelta_str[:-1])
    except ValueError:
        return None
    match multiplicator:
        case "d":
            return timedelta(days=value)
        case "y":
            return timedelta(days=value * 365)
        case "m":
            return timedelta(minutes=value)
        case "h":
            return timedelta(hours=value)
        case "w":
            return timedelta(weeks=value)
    return None


@pin_router.message(
    F.text.regexp(PIN_REGEXP).as_("match"),
    # This magic filter not just link reply_to_message but also check its presence.
    F.reply_to_message.as_("reply"),
)
async def pin_command(message: Message, match: re.Match, reply: Message):
    match = match.groupdict()
    if match["timedelta"]:  # we can access parsed arguments
        delta = timedelta_generator(match["timedelta"])
        await pin_for_time(reply, delta, notify=bool(match["is_notify"]))
    else:
        await pin_message.kiq(chat_id=reply.chat.id, message_id=reply.message_id)
    """Delete message with worker for exception handling (such as potential flood control)"""
    await delete_messages_tg(message)


@pin_router.message(
    F.text.regexp(PIN_REGEXP),
)
async def pin_command(
    message: Message,
):
    """Just remove command on invalid usage."""
    return await delete_messages_tg(message)
