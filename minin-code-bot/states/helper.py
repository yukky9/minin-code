from aiogram.fsm.state import State, StatesGroup


class HelperStates(StatesGroup):
    help = State()
    answer = State()
