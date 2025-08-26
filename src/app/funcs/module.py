import asyncio
import re
from loguru import logger
from uiautomator2 import Device
from app.create_bot import bot
from app.db.dao_models import UserDAO
from app.db.models import User

device = Device("emulator-5554")
# uiautodev
# uiautomatorviewer


class P2PPage:
    def __init__(self, chat_id, min_price):
        self.chat_id = chat_id
        self.min_price = min_price
        self.running = True
        self.last = None

    async def p2p_page(self):
        # find_element_by_path('(//android.widget.TextView)[2]').click()
        # find_element_by_path("//android.widget.ImageView").click()
        # find_element_by_path("(//android.widget.TextView)[6]").click()
        # # how to wait 0.5 sec
        # await asyncio.sleep(0.5)
        # find_element_by_path("(//android.widget.Button)[6]").click()
        # find_element_by_path("//android.widget.Button").click()
        # Получить текст элемента
        for_one = "Не определено"
        username = "Не определено"
        negitioations = "Не определено"
        limits = "Не определено"
        method = "Не определено"
        price_float = 0

        user: User = await UserDAO.get_one_or_none(chat_id=self.chat_id)

        # device.xpath("(//android.widget.ImageButton)[2]").click()
        # await asyncio.sleep(1)

        # device.xpath('//*[@text="Reload Page"]').click()
        # await asyncio.sleep(1)
        # Вставить данные в это поле

        device.xpath('//*[@resource-id="amount"]').set_text(f"{user.amount}")

        def find(i=-3):
            for_one = device.xpath(f"(//android.widget.TextView)[{3+i}]").get_text()
            # print("for one", for_one)
            username = device.xpath(f"(//android.widget.TextView)[{6+i}]").get_text()
            negitioations = device.xpath(
                f"(//android.widget.TextView)[{7+i}]"
            ).get_text()
            limits = device.xpath(f"(//android.widget.TextView)[{11+i}]").get_text()
            method = device.xpath(f"(//android.widget.TextView)[{13+i}]").get_text()
            price_str = for_one.replace(",", ".").replace(" ", "")

            pattern = re.compile(r"[+-]?\d+\.?\d*")
            price_re = re.findall(pattern=pattern, string=price_str)[0]
            # print(price_re)
            price_float = float(price_re)
            print(price_float)
            # print("step1", for_one, username, negitioations, limits, method, price_str)
            return for_one, username, negitioations, limits, method, price_float

        i = -3
        while i < 10:
            try:
                for_one, username, negitioations, limits, method, price_float =  await asyncio.to_thread(find, i)
                break
            except Exception as e:
                logger.error(f"Ошибка в парсинге {e}")
                # try:
                #     for_one, username, negitioations, limits, method, price_float = (
                #         find2(i)
                #     )
                #     break
                # except:
                #     logger.error(f"Ошибка в парсинге2 {e}")
                i += 1

        if price_float < user.price and price_float != self.last:
            self.last = price_float
            await bot.send_message(
                chat_id=self.chat_id,
                text=f"Цена за 1: {for_one}\n"
                f"Имя: {username}\n"
                f"Кол-во сделок: {negitioations}\n"
                f"Лимиты: {limits}\n"
                f"Способ оплаты: {method}\n",
            )

    async def start_func(self):
        self.running = True

    async def stop_func(self):
        self.running = False

    async def change_price(self, price):
        self.min_price = price

    async def run(self):
        while self.running:
            await self.p2p_page()
            await asyncio.sleep(0.1)


# asyncio.run(p2p_page())
