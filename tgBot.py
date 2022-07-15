import logging
import os

from config import API_KEY
from main import get_opp
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def scan_message(message: types.Message):
    await message.answer('Файл получен')

    if message.document.mime_type == 'text/plain':
        file_name = message.document.file_name
        await message.document.download(destination_file=file_name)

        get_opp(file_name)

        await bot.send_document(chat_id=message.from_user.id, document=open(file_name, 'rb'))

        if os.path.isfile(f'temp/{file_name}'):
            os.remove(f'temp/{file_name}')
            print("success")
        else:
            print("File doesn't exists!")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
