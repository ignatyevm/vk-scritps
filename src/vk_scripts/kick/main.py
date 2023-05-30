from vk_scripts import vk
from vk_scripts.config import Config
from vk_scripts import core


def run(user_id: int):
    config = Config()
    tokens = core.read_tokens(config.TOKENS_FILEPATH)
    vk_client = vk.ApiClient(tokens=tokens)
    chat_ids = core.read_chat_ids(config.CHAT_IDS_FILEPATH)
    async with vk_client:
       for chat_id in chat_ids:
           history = vk_client.get_chat_history(chat_id)
           vk_client.kick_user_from_chat(
               chat_id=chat_id,
               user_id=user_id
           )
