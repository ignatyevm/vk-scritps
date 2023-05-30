import logging
import random
from itertools import cycle
from typing import Any

import aiohttp

from .types import *
from .exceptions import ApiError


logger = logging.getLogger("vk-scripts.vk_client")


class ApiClient:
    def __init__(
        self,
        *,
        tokens: list[AccessToken],
        version: float = 5.103
    ):
        self.http_session = None
        self.tokens_iter = cycle(iter(tokens))
        self.version = version
        self.api_url = "https://api.vk.com"

    async def __aenter__(self):
        self.http_session = aiohttp.ClientSession(base_url=self.api_url)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_session.close()

    async def call_method(
        self,
        method: str,
        *,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        params["access_token"] = next(self.tokens_iter)
        if "v" not in params.keys():
            params["v"] = self.version
        async with self.http_session.get(
                url=f"/method/{method}",
                params=params
        ) as response:
            content = await response.json()
            logger.info(
                "sent request with url %s and response %s",
                response.url,
                content
            )
            if "error" in content.keys():
                error = content["error"]
                raise ApiError(
                    code=error["error_code"],
                    message=error["error_msg"],
                    params=error["request_params"]
                )
            return content["response"]

    async def send_message_to_chat(
        self,
        chat_id: ChatId,
        *,
        text: str | None = None,
        attachments: list[Attachment] | None = None
    ):
        params = {
            "random_id": random.randint(a=0, b=2**30),
            "chat_id": chat_id,
            "message": text
        }
        if attachments is not None and len(attachments) > 0:
            params["attachment"] = [
                str(attachment)
                for attachment in attachments
            ]
        return await self.call_method(
            method="messages.send",
            params=params
        )

    async def kick_user_from_chat(
        self,
        *,
        chat_id: ChatId,
        user_id: UserId
    ):
        params = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        return await self.call_method(
            method="messages.removeChatUser",
            params=params
        )

    async def get_chat_members(
        self,
        chat_id: ChatId,
        *,
        count: int | None = None,
        offset: int | None = None
    ) -> dict[str, Any]:
        params = {
            "peer_id": chat_id
        }
        if count is not None:
            params["count"] = count
        if offset is not None:
            params["offset"] = offset
        return await self.call_method(
            method="messages.getConversationMembers",
            params=params
        )

    async def get_chats(
        self,
        chat_ids: list[ChatId]
    ) -> dict[str, Any]:
        params = {
            "peer_ids": ", ".join([str(chat_id) for chat_id in chat_ids])
        }
        return await self.call_method(
            method="messages.getConversationsById",
            params=params
        )
