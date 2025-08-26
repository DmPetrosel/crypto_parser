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
# print("8305754313:AAGEdSBielqMrBaOY2By7oKgAw1pGXs-ERE")  # PROD
# bot = Bot("8305754313:AAGEdSBielqMrBaOY2By7oKgAw1pGXs-ERE")  # PROD
print("6728457989:AAGKKOXF1P9kAjW9gwN3A7Q5NiEkMTLQMck")  # MY
bot = Bot("6728457989:AAGKKOXF1P9kAjW9gwN3A7Q5NiEkMTLQMck")
dp = Dispatcher(bot=bot, storage=storage)
