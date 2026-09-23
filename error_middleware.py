import logging
import traceback
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

logger = logging.getLogger(__name__)

class ErrorsMidleware(BaseMiddleware):

    def __init__(self, admin_id: int):
        super().__init__()
        self.admin_id = admin_id

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any], Awaitable[Any]]],
            event: TelegramObject,
            data: Dict[str, Any],
        ) -> Any:
            try:
                return await handler(event, data)
            except Exception as er:

                logger.error(f"Ошибка: {er}")
                logger.error(traceback.format_exc())

                bot = data.get("bot")

                if bot and self.admin_id:
                    try:
                        await bot.send_message(
                            chat_id=self.admin_id,
                            text=f"Ошибка в боте!\n\n{type(er).__name__}: {er}"
                        )
                    except Exception:
                        pass

                if isinstance(event, Message):
                    await event.answer(
                        "Просим прощения, что-то пошло не так...\nПопробуйте позже."
                    )
                elif isinstance(event, CallbackQuery):
                    await event.answer(
                        "Что-то не так. Попробуйте позже!",
                        show_alert=True
                    )