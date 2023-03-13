from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    choose_work_place = State()
    add_work_place = State()

    work_place = State()
    work_place_rename = State()
    add_work = State()

    work = State()
    work_rename = State()
    add_work_node = State()

    work_node = State()
    work_node_rename = State()
    photo_before = State()
    photo_after = State()

    add_comment = State()
    comment = State()
