import asyncio
import threading
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, types
from fastapi.params import Security
from loguru import logger
from app.create_bot import bot
from app.db.dao_models import UserDAO
from app.db.models import User
from app.funcs.module import P2PPage
from app.keyboards import kb_main
from app.stages.states import RegForm, SecurityState
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.methods import SetMyCommands
from app.utils.utils import tasks, P2pObjects
from traceback import print_exc
from config import config


async def set_menu_commands():
    commands = [
        types.BotCommand(command="/start", description="начало работы"),
        types.BotCommand(command="/settings", description="Настройки"),
    ]
    await bot(SetMyCommands(commands=commands))


async def start(
    message: types.Message,
    state: FSMContext,
):
    await set_menu_commands()
    await state.clear()
    await bot.send_message(
        message.from_user.id,
        "Приветствую! Это бот для парсинга кошелька, сделайте настройки и нажмите Начать. Но прежде введи пароль",
        reply_markup=await kb_main.start_and_stop_kb(),
    )
    await state.set_state(SecurityState.password)


async def check_user(chat_id, message: types.Message, state):
    user = await UserDAO.get_one_or_none(chat_id=chat_id)
    logger.info(f"Пользователь {user}")

    if not user:
        user = await UserDAO.add_by_kwargs(
            chat_id=chat_id, username=message.from_user.username
        )
        logger.info(f"Пользователь {user} создан")
        tasks[user.chat_id] = asyncio.create_task(
            P2PPage(user.chat_id, user.amount).run()
        )


async def init_when_restart():
    user: User
    try:
        for user in await UserDAO.get_all_by_kwargs():
            tasks[user.chat_id] = asyncio.create_task(
                P2PPage(user.chat_id, user.amount).run()
            )
    except Exception as e:
        logger.info(f"NO USERS {e} {print_exc()}")


async def start_callbacks(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(**data)
    if call.data.startswith("stagestart_banks_"):
        bank = call.data.split("_")[-1]
        if not isinstance(data["banks"], list):
            data["banks"] = []
        if bank in data["banks"]:
            data["banks"].remove(bank)
        else:
            data["banks"].append(bank)
        await state.update_data(**data)
        await call.message.edit_text(
            "Выберите банки",
            reply_markup=await kb_main.banks_kb(
                chat_id=call.from_user.id, banks=data["banks"]
            ),
        )
    elif call.data.startswith("stagestart_cancel"):
        await bot.send_message(
            call.from_user.id,
            "Отменено",
            reply_markup=await kb_main.start_and_stop_kb(),
        )
        await state.clear()
    elif call.data == "stagestart_settings_price":
        await bot.send_message(
            call.from_user.id, "Введите цену", reply_markup=kb_main.cancel_kb()
        )
        await state.set_state(RegForm.price)
    elif call.data == "stagestart_settings_amount":
        await bot.send_message(
            call.from_user.id, "Введите сумму", reply_markup=kb_main.cancel_kb()
        )
        await state.set_state(RegForm.amount)
    elif call.data == "stagestart_settings_banks":
        user: User = await UserDAO.get_one_or_none(chat_id=call.from_user.id)
        if user.currency == None:
            await bot.send_message(
                call.from_user.id, "Введите валюту", reply_markup=kb_main.cancel_kb()
            )
            await state.set_state(RegForm.currency)
        banks = user.banks
        await bot.send_message(
            call.from_user.id,
            "Выберите банки",
            reply_markup=await kb_main.banks_kb(chat_id=call.from_user.id, banks=banks),
        )
        await bot.send_message(
            call.from_user.id,
            f"Выберите банки для валюты {user.currency}",
            reply_markup=await kb_main.banks_kb(chat_id=call.from_user.id),
        )
    elif call.data.startswith("stagestart_settings_dimension"):
        await call.message.answer("Введите минимальный диапазон: ")
        await state.set_state(RegForm.dimension)


async def start_or_stop(message: types.Message, state: FSMContext):
    if message.text == "Начать":
        try:
            _ = tasks[message.from_user.id]
        except:
            P2pObjects[message.from_user.id] = P2PPage(
                chat_id=message.from_user.id, min_price=82
            )
            tasks[message.from_user.id] = asyncio.create_task(
                P2pObjects[message.from_user.id].run()
            )
        await P2pObjects[message.from_user.id].start_func()
        await message.answer("Начато", reply_markup=await kb_main.start_and_stop_kb())
    elif message.text == "Стоп":
        await P2pObjects[message.from_user.id].stop_func()
        await message.answer(
            "Остановлено", reply_markup=await kb_main.start_and_stop_kb()
        )


async def settings_func(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.from_user.id, "Настройки", reply_markup=await kb_main.settings_kb()
    )


async def get_price(message: types.Message, state: FSMContext):
    user: User = await UserDAO.get_one_or_none(chat_id=message.from_user.id)
    pr = message.text.replace(",", ".").replace(" ", "")
    try:
        pr = float(pr)
    except:
        await message.answer(
            "Неправильный ввод. Введите число, например 81.05",
            reply_markup=kb_main.cancel_kb(),
        )
        await state.set_state(RegForm.price)
    try:
        await UserDAO.update_by_id(id_=user.id, price=pr)
        await message.answer(f"Цена установлена на {message.text}")
    except Exception as e:
        logger.error(f"Ошибка при изменении цены {e}")
        await message.answer("Ошибка при изменении цены")


async def get_amount(message: types.Message, state: FSMContext):
    user: User = await UserDAO.get_one_or_none(chat_id=message.from_user.id)
    pr = message.text.replace(",", ".").replace(" ", "")
    try:
        pr = float(pr)
    except:
        await message.answer(
            "Неправильный ввод. Введите число, например 81.05",
            reply_markup=kb_main.cancel_kb(),
        )
        await state.set_state(RegForm.amount)
    await UserDAO.update_by_id(id_=user.id, amount=pr)
    await message.answer(f"Сумма для обмена установлена на {message.text}")


async def get_currency(message: types.Message, state: FSMContext):
    user: User = await UserDAO.get_one_or_none(chat_id=message.from_user.id)
    pr = message.text.strip().upper()
    await UserDAO.update_by_id(user.id, amount=pr)
    await message.answer(
        f"Валюта установлена для поиска установлена на {pr}. \n",
    )


async def get_dimension(message: types.Message, state: FSMContext):
    user: User = await UserDAO.get_one_or_none(chat_id=message.from_user.id)
    dim = message.text.replace(",", ".").replace(" ", "")
    try:
        dim = float(dim)
    except:
        await message.answer(
            "Неправильный ввод. Введите число, например 81.05",
            reply_markup=kb_main.cancel_kb(),
        )
        await state.set_state(RegForm.dimension)
    await UserDAO.update_by_id(id_=user.id, dimension=dim)
    await message.answer(f"Минимальная сумма для обмена установлена на {message.text}")


async def get_password(message: types.Message, state: FSMContext):
    if message.text == config.get("bot", "password"):
        await message.answer("Пароль верный")
        await check_user(chat_id=message.from_user.id, message=message, state=state)

    else:
        await message.answer("Пароль НЕ верный, введите ещё раз")
        await state.set_state(SecurityState.password)


def register_handlers_start(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(settings_func, Command("settings"))
    dp.message.register(get_price, StateFilter(RegForm.price))
    dp.message.register(get_amount, StateFilter(RegForm.amount))
    dp.message.register(get_password, StateFilter(SecurityState.password))
    dp.message.register(get_currency, StateFilter(RegForm.currency))
    dp.message.register(get_dimension, StateFilter(RegForm.dimension))
    dp.message.register(start_or_stop, lambda m: m.text == "Начать" or m.text == "Стоп")
    dp.callback_query.register(
        start_callbacks, lambda c: c.data.startswith("stagestart")
    )
