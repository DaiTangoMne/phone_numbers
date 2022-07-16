import logging
import os

from config import API_KEY
from main import get_opp, file_edit
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters

API_TOKEN = API_KEY
PHONE_REGEXP = r'^\+7|8\D*\d{3}\D*\d{3}\D*\d{2}\D*\d{2}'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("<b>Привет!</b>\n\n"
                        "Данный бот определяет оператора по номеру телефона.\n\n"
                        "Для этого напиши боту номер телефона или отправь <i>файл.txt</i> "
                        "с несколькими номерами телефона!", parse_mode="HTML")


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def scan_message(message: types.Message):
    await message.answer('Файл получен')

    if message.document.mime_type == 'text/plain':
        file_name = message.document.file_name
        await message.document.download(destination_file=file_name)

        file_edit(file_name)

        await bot.send_document(chat_id=message.from_user.id, document=open(file_name, 'rb'))

        if os.path.isfile(file_name):
            os.remove(file_name)
            print("success")
        else:
            print("File doesn't exists!")


@dp.message_handler(regexp=PHONE_REGEXP)
async def regexp_example(message: types.Message):
    await message.answer(get_opp(message.text))


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Сообщение не распознано')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
