import dataclasses
import enum
from typing import TypeVar

UserId = TypeVar("UserId")
GroupId = TypeVar("GroupId")
ChatId = TypeVar("ChatId")
PostId = TypeVar("PostId")
PhotoId = TypeVar("PhotoId")
MediaID = PostId | PhotoId

AccessToken = TypeVar("AccessToken")


class AttachmentType(enum.Enum):
    WALL = "wall"


@dataclasses.dataclass
class Attachment:
    type: AttachmentType
    owner_id: UserId | GroupId
    media_id: MediaID

    def __str__(self) -> str:
        return "{}{}_{}".format(
            self.type.value,
            self.owner_id,
            self.media_id
        )