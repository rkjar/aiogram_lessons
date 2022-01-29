import os
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def button_input(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = "Специальные кнопки"
    button_2 = "Написать и удалить"
    keyboard.add(button_1, button_2)
    await message.answer("Проверим кнопки?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Написать и удалить"))
async def button_remover(message: types.Message):
    await message.reply("Прощайте, кнопки!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Специальные кнопки"))
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
    keyboard.add(types.KeyboardButton(text="Запросить контакт", request_contact=True))
    keyboard.add(types.KeyboardButton(text="Создать викторину",
                                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    await message.answer("Выберите действие:", reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp)