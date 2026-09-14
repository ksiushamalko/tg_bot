from datetime import datetime, time
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
class NightModeMiddleware(BaseMiddleware):
    def __init__(self, start_hour: int = 23, end_hour: int = 7):
        super().__init__()
        self.start = time(start_hour, 0)
        self.end = time(end_hour, 0)
    def _is_night(self) -> bool:
        now = datetime.now().time()
        if self.start <= self.end:
            return self.start <= now <= self.end
        return now >= self.start or now <= self.end
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if self._is_night():
            msg = None
            if isinstance(event, Message):
                msg = event
            else:
                msg = getattr(event, "message", None)
            if msg is not None:
                await msg.answer(
                    "Бот спит с 23:00 до 07:00. Пожалуйста, напишите утром"
                )
                return
        return await handler(event, data)