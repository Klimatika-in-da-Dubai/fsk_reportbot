from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    menu = State()
    work = State()
    work_node = State()
    photo_before = State()
    work_node_add = State()
    photo_after = State()

    comment_add = State()
    comment = State()
