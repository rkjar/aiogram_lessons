import os
import logging
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
user_data = {}


def get_keyboard() -> types.InlineKeyboardMarkup:
    # Генерация клавиатуры
    buttons = [types.InlineKeyboardButton(text="-1", callback_data="num_dec"),
               types.InlineKeyboardButton(text="+1", callback_data="num_inc"),
               types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    with suppress(MessageNotModified):
        await message.edit_text(f"Укажите число: {new_value}", reply_markup=get_keyboard())


@dp.message_handler(commands="numbers")
async def numbers_command(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())


@dp.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "inc":
        user_data[call.from_user.id] = user_value + 1
        await update_num_text(call.message, user_value + 1)
    elif action == "dec":
        user_data[call.from_user.id] = user_value - 1
        await update_num_text(call.message, user_value - 1)
    elif action == "finish":
        await call.message.edit_text(f"Итого: {user_value}")
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp)