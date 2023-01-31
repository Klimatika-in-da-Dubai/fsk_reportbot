from aiogram import types

from src.models.report import Report
from src.models.work import Work

from loader import users


def get_user_report(chat_id: int) -> Report:
    return users[chat_id]


def get_last_user_work(chat_id: int) -> Work:
    report = get_user_report(chat_id)
    return report.last_work()
