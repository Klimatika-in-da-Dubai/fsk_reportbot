from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from src.utils.getters import get_user_report


class MenuCB(CallbackData, prefix="menu"):
    action: str


def get_menu_keyboard(chat_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    report = get_user_report(chat_id)

    if report.empty() or not report.last_work.empty():
        builder.add(
            types.InlineKeyboardButton(
                text="Добавить работу", callback_data=MenuCB(action="add_work").pack()
            )
        )

    if not report.empty() and not report.last_work.empty():
        builder.add(
            types.InlineKeyboardButton(
                text="Создать отчёт",
                callback_data=MenuCB(action="generate_report").pack(),
            ),
        )

    builder.adjust(1)
    return builder.as_markup()


def get_yes_no_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons = [
        types.InlineKeyboardButton(
            text="Да", callback_data=MenuCB(action="yes").pack()
        ),
        types.InlineKeyboardButton(
            text="Нет", callback_data=MenuCB(action="no").pack()
        ),
    ]

    builder.add(*buttons)
    builder.adjust(2)
    return builder.as_markup()
