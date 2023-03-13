from aiogram import types

from src.models import User, Report

from loader import users


def get_user(chat_id: int) -> User:
    return users[chat_id]


def get_user_report(chat_id: int) -> Report:
    return users[chat_id].report
