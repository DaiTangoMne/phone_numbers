from aiogram import Bot, Dispatcher, executor
from config import API_KEY

API_TOKEN = API_KEY

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
