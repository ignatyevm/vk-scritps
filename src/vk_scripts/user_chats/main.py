import asyncio

from vk_scripts import core, vk
from vk_scripts.config import Config


async def run(user_id: int):
    config = Config()
    tokens = core.read_tokens(config.TOKENS_FILEPATH)
    vk_client = vk.ApiClient(tokens=tokens)
    chat_ids = core.read_chat_ids(config.CHAT_IDS_FILEPATH)
    async with vk_client:
        chats_members = await asyncio.gather(*[
            vk_client.get_chat_members(chat_id)
            for chat_id in chat_ids
        ])
        for chat_members in chats_members:
            chat_member_ids = [
                chat_member["member_id"]
                for chat_member in chat_members["items"]
            ]
            if user_id in chat_member_ids:
                user_chat_ids.append(user_id)
            user_chat_ids = [

            ]

