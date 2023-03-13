from aiogram import Router

from src.handlers.base import base_router
from src.handlers.menu import (
    choose_work_place_router,
    work_place_router,
    work_router,
    work_node_router,
)

handlers_router = Router()
handlers_router.include_router(base_router)
handlers_router.include_router(choose_work_place_router)
handlers_router.include_router(work_place_router)
handlers_router.include_router(work_router)
handlers_router.include_router(work_node_router)
