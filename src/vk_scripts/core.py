from vk_scripts import vk


def read_tokens(tokens_filepath: str) -> list[vk.AccessToken]:
    with open(tokens_filepath, "r") as tokens_files:
        return [token for token in tokens_files.readlines()]


def read_chat_ids(chat_ids_filepath: str) -> list[int]:
    with open(chat_ids_filepath, "r") as chat_ids_file:
        return [int(chat_id) for chat_id in chat_ids_file.readlines()]
