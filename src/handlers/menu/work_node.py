from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from src.keyboards.menu import (
    WorkNodeCB,
    Action,
    get_work_keyboard,
    get_work_node_keyboard,
)
from src.models import Work, WorkNode

from src.utils.getters import get_user

from src.states.menu import MenuState


work_node_router = Router()


@work_node_router.callback_query(
    MenuState.work_node, WorkNodeCB.filter(F.action == Action.RENAME)
)
async def callback_rename_work_place(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkNodeCB
):
    await callback.answer()

    await state.set_state(MenuState.work_node_rename)
    await callback.message.answer("Введите новое имя для узла работы")


@work_node_router.message(MenuState.work_node_rename, F.text)
async def work_place_rename(message: types.Message, state: FSMContext):
    work_node = get_user(message.chat.id).selected_work_node
    work_node.name = message.text

    await state.set_state(MenuState.work_node)
    await message.answer(
        f"Узел работы: {work_node.name}",
        reply_markup=get_work_node_keyboard(work_node),
    )


@work_node_router.callback_query(
    MenuState.work_node, WorkNodeCB.filter(F.action == Action.ADD_PHOTO)
)
async def callback_rename_work_place(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkNodeCB
):
    await callback.answer()

    await state.set_state(MenuState.photo_before)
    await callback.message.answer("Отправьте 1 фото ДО")


@work_node_router.message(MenuState.photo_before, F.photo)
async def work_place_rename(message: types.Message, state: FSMContext):
    work_node = get_user(message.chat.id).selected_work_node
    work_node.photo_before = message.photo[-1]

    await state.set_state(MenuState.photo_after)
    await message.answer("Отправьте 1 фото ПОСЛЕ")


@work_node_router.message(MenuState.photo_after, F.photo)
async def work_place_rename(message: types.Message, state: FSMContext):
    work_node = get_user(message.chat.id).selected_work_node
    work_node.photo_after = message.photo[-1]

    await state.set_state(MenuState.work_node)
    await message.answer(
        f"Узел работы: {work_node.name}",
        reply_markup=get_work_node_keyboard(work_node),
    )


@work_node_router.callback_query(
    MenuState.work_node, WorkNodeCB.filter(F.action == Action.BACK)
)
async def callback_work_place_back(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkNodeCB
):
    await callback.answer()
    user = get_user(callback.message.chat.id)
    user.selected_work_node = None

    await state.set_state(MenuState.work)
    await callback.message.edit_text(
        f"Работа: {user.selected_work.name}",
        reply_markup=get_work_keyboard(user.selected_work),
    )
