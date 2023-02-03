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
from src.services import pdfreport
from src.utils.utils import create_report_dict

from datetime import datetime

from loader import users

base_router = Router()


@base_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id] = Report()
    await cmd_menu(message, state)


@base_router.message(Command(commands=["/menu"]))
async def cmd_menu(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.menu)
    await message.answer(
        "Выберите действие", reply_markup=get_menu_keyboard(message.chat.id)
    )


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

    await state.set_state(Form.work_node)
    await message.answer("Введите название для узла работы")


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

    await state.set_state(Form.work_node_add)
    await message.answer("Добавить работу?", reply_markup=get_yes_no_keyboard())


@base_router.callback_query(Form.work_node_add, MenuCB.filter(F.action == "yes"))
async def cb_add_work_node(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()

    await state.set_state(Form.work_node)
    await callback.message.answer("Введите название для узла работы")


async def photo_after(message: types.Message, state: FSMContext):
    report = get_user_report(message.chat.id)

    await state.set_state(Form.photo_after)
    await message.answer(f"Фото работы ПОСЛЕ для {report.last_work.current_node.name}")


@base_router.callback_query(Form.work_node_add, MenuCB.filter(F.action == "no"))
async def cb_add_work_node(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await photo_after(callback.message, state)


@base_router.message(Form.photo_after, F.photo)
async def process_photo_after(message: types.Message, state: FSMContext):
    report = get_user_report(message.chat.id)
    work_node = report.last_work.current_node
    work_node.photo_after = message.photo[-1]

    await state.set_state(Form.comment_add)
    await message.answer("Добавить комментарий?", reply_markup=get_yes_no_keyboard())


@base_router.callback_query(Form.comment_add, MenuCB.filter(F.action == "yes"))
async def cb_comment_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Form.comment)
    await callback.message.edit_text("Введите комментарий")


@base_router.message(Form.comment, F.text)
async def process_comment(message: types.Message, state: FSMContext):
    # TODO: прописать валидацию
    warnings.warn("Do validation for comment", FutureWarning)

    report = get_user_report(message.chat.id)
    work_node = report.last_work.current_node
    work_node.comment = message.text

    report.last_work.next()
    if report.last_work.current_node is not None:
        await photo_after(message, state)
        return

    await cmd_menu(message, state)


@base_router.callback_query(Form.comment_add, MenuCB.filter(F.action == "no"))
async def cb_comment_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    report = get_user_report(callback.message.chat.id)

    report.last_work.next()
    if report.last_work.current_node is not None:
        await photo_after(callback.message, state)
        return

    await state.set_state(Form.menu)
    await callback.message.edit_text(
        "Выберите действие",
        reply_markup=get_menu_keyboard(callback.message.chat.id),
    )


@base_router.callback_query(Form.menu, MenuCB.filter(F.action == "generate_report"))
async def cb_generate_report(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):

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
