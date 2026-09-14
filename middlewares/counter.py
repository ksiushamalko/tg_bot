from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
class CounterMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.users: Dict[int, int] = {}
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            msg = getattr(event, "message", None) or getattr(event, "callback_query", None)
            if msg is not None:
                user = msg.from_user
        if user is not None:
            self.users[user.id] = self.users.get(user.id, 0) + 1
            data["user_count"] = self.users[user.id]
            print(f">>> [Counter] user_id={user.id}, count={self.users[user.id]}")
        return await handler(event, data)