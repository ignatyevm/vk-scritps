import asyncio
import logging

import yaml

from vk_scripts import vk
from .models import Script, Template, Timing
from .scheduler import Scheduler


logger = logging.getLogger("vk-scripts.broadcaster.sender")


def parse_all_scripts(broadcast_config_path: str) -> list[Script]:
    with open(broadcast_config_path, "r") as broadcast_config_file:
        data = yaml.load(broadcast_config_file, yaml.Loader)
    return [
        Script(
            chat_ids=script["chat_ids"],
            templates=[
                Template(
                    text=template["text"],
                    attachments=
                        [
                            vk.Attachment(
                                type=vk.AttachmentType[attachment["type"].upper()],
                                owner_id=attachment["owner_id"],
                                media_id=attachment["media_id"]
                            )
                            for attachment in template["attachments"]
                        ]
                        if "attachments" in template
                        else None
                )
                for template in script["templates"]
            ],
            timings=[
                Timing(
                    hour=int(timing["time"].split(":")[0]),
                    minute=int(timing["time"].split(":")[1]),
                    weekday=timing["weekday"]
                    if "weekday" in timing
                    else None
                )
                for timing in script["timings"]
            ]
        )
        for script in data["scripts"]
    ]


class ChatBroadcaster:
    def __init__(
        self,
        *,
        broadcast_config_path: str,
        vk_client: vk.ApiClient,
        scheduler: Scheduler
    ):
        self.broadcast_config_path = broadcast_config_path
        self.vk_client = vk_client
        self.scheduler = scheduler


    async def start_broadcasting(self):
        scripts = parse_all_scripts(self.broadcast_config_path)
        for script in scripts:
            for timing in script.timings:
                self.scheduler.register_task(timing, self.make_sender(script))
        await self.scheduler.run()

    def make_sender(self, script: Script):
        async def sender():
            template = script.next_template()
            logger.info("sending %s to %s chats", template, script.chat_ids)

            tasks = []
            for chat_id in script.chat_ids:
                tasks.append(
                    self.vk_client.send_message_to_chat(
                        chat_id=chat_id,
                        text=template.text,
                        attachments=template.attachments
                    )
                )
            await asyncio.gather(*tasks)

            logger.info("sent %s to %s chats", template, script.chat_ids)

        return sender()

