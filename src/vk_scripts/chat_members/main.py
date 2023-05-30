import asyncio

from vk_scripts import core, vk
from vk_scripts.config import Config
from openpyxl import Workbook


async def run(output_filepath: str):

    config = Config()
    tokens = core.read_tokens(config.TOKENS_FILEPATH)
    vk_client = vk.ApiClient(tokens=tokens)
    chat_ids = core.read_chat_ids(config.CHAT_IDS_FILEPATH)

    async with vk_client:
        chats = await vk_client.get_chats(chat_ids)
        chat_names = {
            chat["peer"]["id"]: chat["chat_settings"]["title"]
            for chat in chats["items"]
        }

        wb = Workbook()

        async def save_members(chat_id: vk.ChatId):
            chat_members = await vk_client.get_chat_members(chat_id)
            ws = wb.create_sheet(chat_names[chat_id])
            for chat_member in chat_members["items"]:
                ws.append(chat_member["member_id"])

        await asyncio.gather(*[
            save_members(chat_id)
            for chat_id in chat_ids
        ])

        wb.save(output_filepath)

    # with open(output_filepath, "w") as file:
    #     file.writelines([f"{member_id}\n" for member_id in member_ids])
