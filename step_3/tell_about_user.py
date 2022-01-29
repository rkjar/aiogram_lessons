import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Узнать", callback_data="get_user_info"))
    await message.answer("Что знает телеграм про тебя", reply_markup=keyboard)


@dp.callback_query_handler(text="get_user_info")
async def send_user_info(call: types.CallbackQuery):
    await call.message.answer(str(f"Ваш user id: <b>{call.from_user.id}</b>\n"
                                  f"Ваш user name: <b>{call.from_user.username}</b>\n"
                                  f"Ваш установленный язык: <b>{call.from_user.language_code}</b>"))
    await call.answer()


@dp.message_handler()
async def about(message: types.Message):
    await message.answer(text="Print <b>/start</b> to get started the bot experience.")


if __name__ == "__main__":
    executor.start_polling(dp)