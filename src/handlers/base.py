import warnings

from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.utils.chat_action import ChatActionSender

from src.models.report import Report
from src.models.work import Work
from src.models.work_node import WorkNode
from src.keyboards.menu import MenuCB, get_menu_keyboard, get_yes_no_keyboard
from src.utils.states import Form
from src.utils.getters import get_user_report

from loader import users

base_router = Router()


@base_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id] = Report()
    await cmd_menu(message, state)


@base_router.message(Command(commands=["/menu"]))
async def cmd_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.menu)
    await message.answer("Выберите действие", reply_markup=get_menu_keyboard())


@base_router.callback_query(Form.menu, MenuCB.filter(F.action == "add_work"))
async def cb_add_work(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Form.work)
    await callback.message.answer("Введите название для работы")


@base_router.message(Form.work, F.text)
async def process_work_name(message: types.Message, state: FSMContext):
    # TODO: прописать валидацию
    warnings.warn("Do validation for work_name", FutureWarning)
    report = get_user_report(message.chat.id)
    report.add_work(Work(message.text))

    await cmd_menu(message, state)


@base_router.callback_query(Form.menu, MenuCB.filter(F.action == "add_work_node"))
async def cb_add_work_node(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Form.work_node)
    await callback.message.answer("Введите название для узла работы")


@base_router.message(Form.work_node, F.text)
async def process_work_node_name(message: types.Message, state: FSMContext):
    # TODO: прописать валидацию
    warnings.warn("Do validation for work_node_name", FutureWarning)
    report = get_user_report(message.chat.id)
    work = report.last_work
    work.add_work_node(WorkNode(name=message.text))

    await state.set_state(Form.photo_before)
    await message.answer("Фото работы ДО")


@base_router.message(Form.photo_before, F.photo)
async def process_photo_before(message: types.Message, state: FSMContext):
    report = get_user_report(message.chat.id)
    work_node = report.last_work_node
    work_node.photo_before = message.photo[-1]

    await state.set_state(Form.photo_after)
    await message.answer("Фото работы ПОСЛЕ")


@base_router.message(Form.photo_after, F.photo)
async def process_photo_after(message: types.Message, state: FSMContext):
    report = get_user_report(message.chat.id)
    work_node = report.last_work_node
    work_node.photo_after = message.photo[-1]

    await state.set_state(Form.comment)
    await message.answer("Добавить комментарий?", reply_markup=get_yes_no_keyboard())


@base_router.callback_query(Form.comment, MenuCB.filter(F.action == "yes"))
async def cb_comment_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text("Введите комментарий")


@base_router.message(Form.comment, F.text)
async def process_comment(message: types.Message, state: FSMContext):
    # TODO: прописать валидацию
    warnings.warn("Do validation for comment", FutureWarning)

    report = get_user_report(message.chat.id)
    work_node = report.last_work_node
    work_node.comment = message.text

    await cmd_menu(message, state)


@base_router.callback_query(Form.comment, MenuCB.filter(F.action == "no"))
async def cb_comment_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Form.menu)
    await callback.message.edit_text(
        "Выберите действие", reply_markup=get_menu_keyboard()
    )


@base_router.callback_query(Form.menu, MenuCB.filter(F.action == "generate_report"))
async def cb_generate_report(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    await callback.answer()

    await state.clear()
    async with ChatActionSender.upload_document(callback.message.chat.id, bot=bot):
        await callback.message.answer("Генерируем отчёт")
