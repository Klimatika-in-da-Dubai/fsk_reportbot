import warnings

from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.utils.chat_action import ChatActionSender

from src.models import User
from src.keyboards.menu import get_choose_work_places_keyboard
from src.utils.getters import get_user_report


from src.states.menu import MenuState


from loader import users

base_router = Router()


@base_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id] = User()
    await cmd_menu(message, state)


@base_router.message(Command(commands=["/menu"]))
async def cmd_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(MenuState.choose_work_place)
    await message.answer(
        "Можете добавить место работы или создать отчёт",
        reply_markup=get_choose_work_places_keyboard(get_user_report(message.chat.id)),
    )
