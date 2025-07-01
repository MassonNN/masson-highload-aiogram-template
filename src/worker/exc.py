from aiogram.exceptions import *

CannotPerfromRetry = (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramUnauthorizedError,
)

CanPerformRetry = (TelegramRetryAfter, RestartingTelegram, TelegramConflictError)