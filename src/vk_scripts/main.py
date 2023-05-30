import asyncio
import logging
import logging.handlers
from functools import wraps

import click

from vk_scripts import broadcaster, chat_members


logger = logging.getLogger("vk-scripts")
handler = logging.handlers.TimedRotatingFileHandler(
    filename="logs/vk-scripts.log",
    when='d',
    interval=10,
    backupCount=10
)
formatter = logging.Formatter(
        '%(asctime)s | %(name)-25s | %(levelname)-6s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger = logging.getLogger("vk-scripts.main")


def async_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@click.group
@async_command
async def vk_scripts_cli():
    pass


@vk_scripts_cli.command("broadcast")
@click.argument(
    'broadcast_config_path',
    type=click.Path(exists=True, readable=True, resolve_path=True),
    default="broadcast_config.yml"
)
@async_command
async def broadcaster_command_handler(broadcast_config_path: str):
    click.echo("Broadcaster started")
    await broadcaster.run(broadcast_config_path)


@vk_scripts_cli.command("kick")
@click.argument("user_id", type=click.INT)
@async_command
async def kick_command_handler(user_id: int):
    click.echo("{} kicked".format(user_id))


@vk_scripts_cli.command("chat-members")
@click.argument(
    'output_filepath',
    type=click.Path(resolve_path=True),
    default="chat_members.xlsx"
)
@async_command
async def chat_members_command_handler(output_filepath: str):
    click.echo("Loading users...")
    await chat_members.run(output_filepath)
    click.echo("Success!")


if __name__ == "__main__":
    vk_scripts_cli()
