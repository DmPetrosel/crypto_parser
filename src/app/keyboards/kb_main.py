from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from app.db.dao_models import UserDAO
from app.db.models import User
import math
from app.utils.utils import tasks


async def start_and_stop_kb():
    kb = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    # kb.keyboard.append([KeyboardButton(text="Начать"), KeyboardButton(text="Стоп")])
    kb = ReplyKeyboardRemove()
    return kb


async def settings_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.extend(
        [
            [
                InlineKeyboardButton(
                    text="Цена", callback_data="stagestart_settings_price"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Сумма", callback_data="stagestart_settings_amount"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Минимальная для обмена",
                    callback_data="stagestart_settings_dimension",
                )
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Банки", callback_data="stagestart_settings_banks"
            #     )
            # ],
            # [
            #     InlineKeyboardButton(
            #         text="Скрыть настройки", callback_data="stagestart_canc"
            #     )
            # ],
        ]
    )
    return kb


def cancel_kb():
    # TODO make cancel Callback
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append(
        [InlineKeyboardButton(text="Отмена", callback_data=f"stagestart_cancel")]
    )
    return kb
