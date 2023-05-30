import asyncio
import logging

from vk_scripts import vk, core
from vk_scripts.config import Config


logger = logging.getLogger("vk-scripts")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s | %(name)-25s | %(levelname)-6s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger = logging.getLogger("vk-scripts.test")


async def run():
    config = Config()
    tokens = core.read_tokens(config.TOKENS_FILEPATH)
    vk_client = vk.ApiClient(tokens=tokens)
    async with vk_client:
        print(await vk_client.call_method("messages.getConversationMembers", params={
            "peer_id": 2000000003,
            "extended": 1,
            "v": 5.144
        }))
        # tasks = []
        # for i in range(1, 50):
        #     tasks.append(vk_client.get_chat_history(chat_id=1))
        # print(await asyncio.gather(*tasks))


if __name__ == "__main__":
    asyncio.run(run())
