from dataclasses import dataclass
from aiogram import types


@dataclass
class WorkNode:
    name: str
    photo_before: types.PhotoSize | None = None
    photo_after: types.PhotoSize | None = None

    def filled(self) -> bool:
        """
        Return false if any of photo fields is None
        """
        return self.photo_before is not None and self.photo_after is not None
