import logging
import os
import time
from datetime import datetime
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
logger = logging.getLogger(__name__)
LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "bot.log",
)
class LoggingMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        print(">>> [Logging] __call__ ВЫЗВАН, тип события:", type(event).__name__)
        user = data.get("event_from_user")
        text = ""
        if isinstance(event, Message):
            text = event.text or event.caption or "[не текст]"
        elif isinstance(event, CallbackQuery):
            text = f"[callback] {event.data}"
        else:
            msg = getattr(event, "message", None)
            cb = getattr(event, "callback_query", None)
            if msg is not None:
                text = msg.text or msg.caption or "[не текст]"
                if user is None:
                    user = msg.from_user
            elif cb is not None:
                text = f"[callback] {cb.data}"
                if user is None:
                    user = cb.from_user

        print(">>> [Logging] user =", user)
        print(">>> [Logging] text =", repr(text))
        if user is not None:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(f"{now} | user_id={user.id} | text={text}\n")
                print(f">>> [Logging] ЗАПИСАНО в {LOG_PATH}")
            except Exception as e:
                print(f">>> [Logging] ОШИБКА: {e!r}")
        else:
            print(">>> [Logging] user = None, пропускаем")
        start = time.time()
        result = await handler(event, data)
        print(f">>> [Logging] handler выполнен за {time.time() - start:.2f} сек")
        return result