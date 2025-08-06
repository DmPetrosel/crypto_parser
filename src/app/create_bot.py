from aiogram import Dispatcher, types, Bot
import asyncio
import configparser
from aiogram.filters import Command
from aiogram.methods import SetMyCommands
from config.settings import settings

from aiogram.fsm.storage.memory import MemoryStorage
# TODO Use redis for production version. !Note Redis can store ONLY int ans str
# from aiogram.fsm.storage.redis import Redis, RedisStorage
# redis= Redis()
# storage = RedisStorage(redis=redis)
storage = MemoryStorage()
tasks = []
print(settings.BOT_TOKEN)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
