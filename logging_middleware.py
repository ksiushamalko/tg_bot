import logging 
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

logger = logging.getLogger(__name__)

class LoggingMiddleWare(BaseMiddleware): #? Класс для работы с мидлварами (обработка входящих сообщений)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any], Awaitable[Any]]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user = data.get("event_from_user")
        user_info = f"{user.id} @{user.username}"

        if isinstance(event, Message): #? Определяем тип ошибки
            event_type = "Сообщение"
            content = event.text or "<без текста>"
        elif isinstance(event, CallbackQuery):
            event_type = "callback"
            content = event.data
        else:
            event_type = "другое"
            content = "-"

        logger.info(f"[{event_type}] {user_info}: {content}")

        start = time.time()

        try:
            result = await handler(event, data)
            el = time.time() - start

            logger.info(f"Обработано за: {el:.3f} сек.")

            return result
        except Exception as er:
            el = time.time() - start
            logger.error(f"Ошибка за {el: .3f} сек: {er}")
            raise