import dataclasses
import json
from typing import Any


@dataclasses.dataclass
class ApiError(Exception):
    code: int
    message: str
    params: dict[str, Any]

    def __str__(self):
        return json.dumps({
            "code": self.code,
            "message": self.message,
            "prams": self.params
        })