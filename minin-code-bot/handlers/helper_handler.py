from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command
import keyboards
from gateway import get_llama_answer
from states import HelperStates

router = Router()


@router.message(F.text.lower() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за обращение. Сеанс будет закрыт!", reply_markup=ReplyKeyboardRemove())
    await message.answer("Вы вернулись в главное меню", reply_markup=keyboards.start_keyboard())


@router.message(Command("helper"))
async def helper(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите свой вопрос", reply_markup=keyboards.cancel_kb())
    await state.set_state(HelperStates.help)


@router.message(HelperStates.help)
async def answer(message: Message, state: FSMContext):
    ans = get_llama_answer(message.text)
    await message.answer(ans, reply_markup=keyboards.cancel_kb())
    await state.set_state(HelperStates.help)
