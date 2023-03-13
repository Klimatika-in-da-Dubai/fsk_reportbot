from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from src.keyboards.menu import (
    WorkCB,
    Action,
    get_work_place_keyboard,
    get_work_keyboard,
    get_work_node_keyboard,
)
from src.models import Work, WorkNode

from src.utils.getters import get_user

from src.states.menu import MenuState


work_router = Router()


@work_router.callback_query(MenuState.work, WorkCB.filter(F.action == Action.OPEN))
async def callback_open_work(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkCB
):
    await callback.answer()
    user = get_user(callback.message.chat.id)
    user.select_work_node(callback_data.index)

    await state.set_state(MenuState.work_node)
    await callback.message.edit_text(
        text=f"Узел работы: {user.selected_work_node.name}",
        reply_markup=get_work_node_keyboard(user.selected_work),
    )


@work_router.callback_query(MenuState.work, WorkCB.filter(F.action == Action.ADD))
async def callback_add_work(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkCB
):
    await callback.answer()

    await state.set_state(MenuState.add_work_node)
    await callback.message.answer("Введите имя для нового узла работы")


@work_router.message(MenuState.add_work_node, F.text)
async def add_work(message: types.Message, state: FSMContext):
    work: Work = get_user(message.chat.id).selected_work
    work.add_node(WorkNode(message.text))

    await state.set_state(MenuState.work)
    await message.answer(
        f"Работа: {work.name}\nКоментарий: {work.comment}",
        reply_markup=get_work_keyboard(work),
    )


@work_router.callback_query(MenuState.work, WorkCB.filter(F.action == Action.RENAME))
async def callback_rename_work_place(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkCB
):
    await callback.answer()

    await state.set_state(MenuState.work_rename)
    await callback.message.answer("Введите новое имя для работы")


@work_router.message(MenuState.work_rename, F.text)
async def work_place_rename(message: types.Message, state: FSMContext):
    work = get_user(message.chat.id).selected_work
    work.name = message.text

    await state.set_state(MenuState.work)
    await message.answer(
        f"Работа: {work.name}\nКоментарий: {work.comment}",
        reply_markup=get_work_keyboard(work),
    )


@work_router.callback_query(
    MenuState.work, WorkCB.filter(F.action == Action.ADD_COMMENT)
)
async def callback_rename_work_place(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkCB
):
    await callback.answer()

    await state.set_state(MenuState.add_comment)
    await callback.message.answer("Введите коментарий для работы")


@work_router.message(MenuState.add_comment, F.text)
async def work_place_rename(message: types.Message, state: FSMContext):
    work = get_user(message.chat.id).selected_work
    work.comment = message.text

    await state.set_state(MenuState.work)
    await message.answer(
        f"Работа: {work.name}\nКоментарий: {work.comment}",
        reply_markup=get_work_keyboard(work),
    )


@work_router.callback_query(MenuState.work, WorkCB.filter(F.action == Action.BACK))
async def callback_work_place_back(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkCB
):
    await callback.answer()
    user = get_user(callback.message.chat.id)
    user.selected_work = None

    await state.set_state(MenuState.work_place)
    await callback.message.edit_text(
        f"Место работы: {user.selected_work_place.name}",
        reply_markup=get_work_place_keyboard(user.selected_work_place),
    )
