from aiogram import Dispatcher, types, Bot
import asyncio
import configparser
from aiogram.filters import Command
from aiogram.methods import SetMyCommands
from config.settings import settings
from loguru import logger
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
# TODO Use redis for production version. !Note Redis can store ONLY int ans str
# from aiogram.fsm.storage.redis import Redis, RedisStorage
# redis= Redis()
# storage = RedisStorage(redis=redis)
storage = MemoryStorage()
tasks = []
try:
    token = config.get('bot', 'token')  
    bot = Bot(token)
    dp = Dispatcher(bot=bot, storage=storage)
except:
    token = str("\n===================================================================="
        "\n\nЗадайте токен бота из BotFather в файле config.ini по примеру config.ini.example\n"
        "==========================================================================")
logger.info(token)  # MY
