from dataclasses import dataclass
from itertools import cycle

from vk_scripts import vk


@dataclass
class Timing:
    hour: int
    minute: int
    weekday: int | None = None

    def __hash__(self):
        if self.weekday is None:
            return hash((self.hour, self.minute))
        return hash((self.hour, self.minute, self.weekday))


@dataclass
class Template:
    text: str
    attachments: list[vk.Attachment]


@dataclass
class Script:
    chat_ids: list[vk.ChatId]
    templates: list[Template]
    timings: list[Timing]

    def __post_init__(self):
        self.current_template_iter = cycle(self.templates)

    def next_template(self) -> Template:
        return next(self.current_template_iter)
