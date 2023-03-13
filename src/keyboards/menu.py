from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from enum import IntEnum, auto

from src.models import Report, WorkPlace, Work, WorkNode


class Action(IntEnum):
    NOTHING = auto()
    ADD = auto()
    REMOVE = auto()
    POP = auto()
    RENAME = auto()
    OPEN = auto()
    GENERATE = auto()
    BACK = auto()
    ADD_PHOTO = auto()
    ADD_COMMENT = auto()


class MenuCB(CallbackData, prefix="menu"):
    action: Action


class ChooseWorkPlaceCB(CallbackData, prefix="ch_work_place"):
    action: Action
    index: int


class WorkPlaceCB(CallbackData, prefix="work_place"):
    action: Action
    index: int


class WorkCB(CallbackData, prefix="work"):
    action: Action
    index: int


class WorkNodeCB(CallbackData, prefix="work_node"):
    action: Action


def get_choose_work_places_keyboard(report: Report) -> types.InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    for index, work_place in enumerate(report.work_places):
        work_place: WorkPlace

        emoji = "✅" if work_place.filled() else "❌"

        builder.add(
            types.InlineKeyboardButton(
                text=f"{work_place.name} {emoji}",
                callback_data=ChooseWorkPlaceCB(action=Action.OPEN, index=index).pack(),
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text="Добавить место работы",
            callback_data=ChooseWorkPlaceCB(action=Action.ADD, index=-1).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text="Сгенерировать",
            callback_data=ChooseWorkPlaceCB(action=Action.GENERATE, index=-1).pack(),
        )
    )

    builder.adjust(1)
    return builder.as_markup()


def get_work_place_keyboard(work_place: WorkPlace) -> types.InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    for index, work in enumerate(work_place.works):
        work: Work

        emoji = "✅" if work.filled() else "❌"

        builder.add(
            types.InlineKeyboardButton(
                text=f"{work.name} {emoji}",
                callback_data=WorkPlaceCB(action=Action.OPEN, index=index).pack(),
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text="Добавить работу",
            callback_data=WorkPlaceCB(action=Action.ADD, index=-1).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text="Переименовать место работы",
            callback_data=WorkPlaceCB(action=Action.RENAME, index=-1).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text="Назад", callback_data=WorkPlaceCB(action=Action.BACK, index=-1).pack()
        )
    )

    builder.adjust(1)
    return builder.as_markup()


def get_work_keyboard(work: Work) -> types.InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    for index, work_node in enumerate(work.work_nodes):
        work_node: WorkNode

        emoji = "✅" if work_node.filled() else "❌"

        builder.add(
            types.InlineKeyboardButton(
                text=f"{work_node.name} {emoji}",
                callback_data=WorkCB(action=Action.OPEN, index=index).pack(),
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text="Добавить узел работы",
            callback_data=WorkCB(action=Action.ADD, index=-1).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text="Переименовать работу",
            callback_data=WorkCB(action=Action.RENAME, index=-1).pack(),
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text="Добавить коментарий",
            callback_data=WorkCB(action=Action.ADD_COMMENT, index=-1).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text="Назад", callback_data=WorkCB(action=Action.BACK, index=-1).pack()
        )
    )

    builder.adjust(1)
    return builder.as_markup()


def get_work_node_keyboard(work_node: WorkNode) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text="Переименовать", callback_data=WorkNodeCB(action=Action.RENAME).pack()
        )
    )

    add_text = "Изменить фото" if work_node.filled() else "Добавить фото"
    builder.add(
        types.InlineKeyboardButton(
            text=add_text,
            callback_data=WorkNodeCB(action=Action.ADD_PHOTO).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text="Назад",
            callback_data=WorkNodeCB(action=Action.BACK).pack(),
        )
    )

    builder.adjust(1)
    return builder.as_markup()
