from dataclasses import dataclass
from aiogram import types


@dataclass
class WorkNode:
    name: str
    photo_before: types.PhotoSize = None
    photo_after: types.PhotoSize = None
    comment: str = ""
