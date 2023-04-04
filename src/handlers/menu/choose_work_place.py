from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from src.utils.getters import get_user_report, get_user
from src.models import WorkPlace

from src.keyboards.menu import (
    ChooseWorkPlaceCB,
    Action,
    get_choose_work_places_keyboard,
    get_work_place_keyboard,
)

from src.services import pdfreport
from src.utils.utils import create_report_dict
from datetime import datetime


from src.states.menu import MenuState

choose_work_place_router = Router()


@choose_work_place_router.callback_query(
    MenuState.choose_work_place, ChooseWorkPlaceCB.filter(F.action == Action.OPEN)
)
async def callback_open_work_place(
    callback: types.CallbackQuery, state: FSMContext, callback_data: ChooseWorkPlaceCB
) -> None:
    await callback.answer()
    user = get_user(callback.message.chat.id)
    user.select_work_place(callback_data.index)

    await state.set_state(MenuState.work_place)
    await callback.message.edit_text(
        f"Место работы: {user.selected_work_place.name}",
        reply_markup=get_work_place_keyboard(user.selected_work_place),
    )


@choose_work_place_router.callback_query(
    MenuState.choose_work_place, ChooseWorkPlaceCB.filter(F.action == Action.ADD)
)
async def callback_work_place_add(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    await callback.answer()
    await state.set_state(MenuState.add_work_place)
    await callback.message.answer("Введите название для нового места работы")


@choose_work_place_router.message(MenuState.add_work_place, F.text)
async def add_work_place(message: types.Message, state: FSMContext):
    report = get_user_report(message.chat.id)

    report.add_work_place(WorkPlace(message.text))
    await state.set_state(MenuState.choose_work_place)
    await message.answer(
        "Можете добавить место работы или создать отчёт",
        reply_markup=get_choose_work_places_keyboard(report),
    )


@choose_work_place_router.callback_query(
    MenuState.choose_work_place, ChooseWorkPlaceCB.filter(F.action == Action.GENERATE)
)
async def cb_generate_report(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    report = get_user_report(callback.message.chat.id)
    if not report.filled():
        await callback.answer("Вы не заполнили отчёт полностью")
        return

    await callback.answer()
    await state.clear()
    async with ChatActionSender.upload_document(callback.message.chat.id, bot=bot):
        await callback.message.answer("Генерируем отчёт")
        pdf_report_path = await generate_report(bot, callback.message.chat.id)
        await callback.message.answer_document(
            types.FSInputFile(pdf_report_path), caption=("Спасибо за вашу работу!")
        )


async def generate_report(bot: Bot, chat_id: int) -> str:
    report = await create_report_dict(get_user_report(chat_id), bot)
    report_name = f"{chat_id}_{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}"
    pdfreport.pdfGenerator(report_name).generate(report)
    return f"./reports/{report_name}-compressed.pdf"
