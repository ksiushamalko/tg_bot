from typing import Callable, Dict, Any, Awaitable

from aiogram.types import Message, TelegramObject
from aiogram import BaseMiddleware

class AdminMiddleware(BaseMiddleware):

    def __init__(self, admin_ids: list[int]):

        self.admin_ids = admin_ids
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any], Awaitable[Any]]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        user = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        if user.id not in self.admin_ids:
            if isinstance(event, Message):
                await event.answer("У вас отсутствует доступ к данному боту!")
            return

        return await handler(event, data)
        