from pathlib import Path

from pydantic import BaseSettings


ENV_FILEPATH = Path(__file__).parent.parent.parent.joinpath(".env")

class Config(BaseSettings):
    TOKENS_FILEPATH: str
    CHAT_IDS_FILEPATH: str

    class Config:
        env_file = ENV_FILEPATH
