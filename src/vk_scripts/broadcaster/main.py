import asyncio

from vk_scripts import vk
from vk_scripts.config import Config
from .broadcaster import ChatBroadcaster
from .scheduler import Scheduler


async def run(broadcast_config_path):
    config = Config()
    scheduler = Scheduler(asyncio.get_running_loop())

    vk_client = vk.ApiClient(access_token=config.BOT_ACCESS_TOKEN)
    async with vk_client:
        broadcaster = ChatBroadcaster(
            vk_client=vk_client,
            broadcast_config_path=broadcast_config_path,
            scheduler=scheduler
        )
        await broadcaster.start_broadcasting()
