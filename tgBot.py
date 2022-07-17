import logging

from config import ADMIN_ID
from create_bot import dp, bot
from aiogram.utils import executor

from handlers import client, admin, other


async def on_startup(_):
    await bot.send_message(ADMIN_ID, 'Бот запущен!')


logging.basicConfig(level=logging.INFO)
client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
