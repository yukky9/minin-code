import requests
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import GREETING
import keyboards
from api import register_user

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    try:
        register_user(message.from_user.username, message.from_user.id)
        await message.answer(GREETING, reply_markup=keyboards.start_keyboard())
    except requests.exceptions.RequestException:
        await message.answer("Не удалось инециализировать пользователя. Пожалуйста, попробуйте позже")


@router.message()
async def f(message: Message):
    await message.answer("OK")
