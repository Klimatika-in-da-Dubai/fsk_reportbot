from aiogram import Router

from src.handlers.base import base_router


handlers_router = Router()
handlers_router.include_router(base_router)
