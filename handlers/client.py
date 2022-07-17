import os

from create_bot import dp, bot
from aiogram import types, Dispatcher
from main import get_opp, file_edit

from config import PHONE_REGEXP


# @dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("<b>Привет!</b>\n\n"
                        "Данный бот определяет оператора по номеру телефона.\n\n"
                        "Для этого напиши боту номер телефона или отправь <i>файл.txt</i> "
                        "с несколькими номерами телефона!", parse_mode="HTML")


# @dp.message_handler(content_types=types.ContentType.DOCUMENT)
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


# @dp.message_handler(regexp=PHONE_REGEXP)
async def regexp_phone(message: types.Message):
    await message.answer(get_opp(message.text))


# @dp.message_handler()
async def err(message: types.Message):
    await message.answer('Сообщение не распознано')


def register_handlers_client(dp: Dispatcher):
   dp.register_message_handler(send_welcome, commands=['start', 'help'])
   dp.register_message_handler(scan_message, content_types=types.ContentType.DOCUMENT)
   dp.register_message_handler(regexp_phone, regexp=PHONE_REGEXP)
   dp.register_message_handler(err)