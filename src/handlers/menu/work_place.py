from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.keyboards.menu import (
    WorkPlaceCB,
    Action,
    get_choose_work_places_keyboard,
    get_work_place_keyboard,
    get_work_keyboard,
)
from src.models import WorkPlace, Work

from src.utils.getters import get_user


from src.states.menu import MenuState


work_place_router = Router()


@work_place_router.callback_query(
    MenuState.work_place, WorkPlaceCB.filter(F.action == Action.OPEN)
)
async def callback_open_work(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkPlaceCB
):
    await callback.answer()
    user = get_user(callback.message.chat.id)
    user.select_work(callback_data.index)

    await state.set_state(MenuState.work)
    await callback.message.edit_text(
        text=f"Работа: {user.selected_work.name}\nКоментарий: {user.selected_work.comment}",
        reply_markup=get_work_keyboard(user.selected_work),
    )


@work_place_router.callback_query(
    MenuState.work_place, WorkPlaceCB.filter(F.action == Action.ADD)
)
async def callback_add_work(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkPlaceCB
):
    await callback.answer()

    await state.set_state(MenuState.add_work)
    await callback.message.answer("Введите имя для новой работы")


@work_place_router.message(MenuState.add_work, F.text)
async def add_work(message: types.Message, state: FSMContext):
    work_place: WorkPlace = get_user(message.chat.id).selected_work_place
    work_place.add_work(Work(message.text))

    await state.set_state(MenuState.work_place)
    await message.answer(
        f"Место работы: {work_place.name} ",
        reply_markup=get_work_place_keyboard(work_place),
    )


@work_place_router.callback_query(
    MenuState.work_place, WorkPlaceCB.filter(F.action == Action.RENAME)
)
async def callback_rename_work_place(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkPlaceCB
):
    await callback.answer()

    await state.set_state(MenuState.work_place_rename)
    callback.message.answer("Введите новое имя для места работы")


@work_place_router.message(MenuState.work_place_rename, F.text)
async def work_place_rename(message: types.Message, state: FSMContext):
    work_place = get_user(message.chat.id).selected_work_place
    work_place.name = message.text

    await state.set_state(MenuState.work_place)
    await message.answer(
        f"Работа: {work_place.name}",
        reply_markup=get_work_place_keyboard(work_place),
    )


@work_place_router.callback_query(
    MenuState.work_place, WorkPlaceCB.filter(F.action == Action.DELETE)
)
async def callback_delete_work_place(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkPlaceCB
):
    await callback.answer()
    user = get_user(callback.message.chat.id)
    report = user.report
    report.remove_work_place(user.selected_work_place)

    await callback_work_place_back(callback, state, callback_data)


@work_place_router.callback_query(
    MenuState.work_place, WorkPlaceCB.filter(F.action == Action.BACK)
)
async def callback_work_place_back(
    callback: types.CallbackQuery, state: FSMContext, callback_data: WorkPlaceCB
):
    await callback.answer()
    user = get_user(callback.message.chat.id)
    user.selected_work_place = None

    await state.set_state(MenuState.choose_work_place)
    await callback.message.edit_text(
        "Можете добавить место работы или создать отчёт",
        reply_markup=get_choose_work_places_keyboard(user.report),
    )
