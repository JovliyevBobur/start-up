"""
Qishloq-AI Anti-Flood Middleware
"""
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
import time


class ThrottlingMiddleware(BaseMiddleware):
    """Xabar tezligini cheklash"""

    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.user_last_message: Dict[int, float] = {}
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.user_last_message:
            elapsed = current_time - self.user_last_message[user_id]
            if elapsed < self.rate_limit:
                return  # Ignore too-fast messages

        self.user_last_message[user_id] = current_time
        return await handler(event, data)
