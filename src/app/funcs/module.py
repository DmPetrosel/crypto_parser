import asyncio
import re
from loguru import logger
from uiautomator2 import Device
from app.create_bot import bot
from app.db.dao_models import UserDAO
from app.db.models import User

device = Device("emulator-5554")
# uiautodev
# weditor
# uiautomatorviewer


class P2PPage:
    def __init__(self, chat_id, min_price):
        self.chat_id = chat_id
        self.min_price = min_price
        self.running = True
        self.last = []

    async def p2p_page(self):
        for_one = "Не определено"
        username = "Не определено"
        negatiotions = "Не определено"
        limits = "Не определено"
        method = "Не определено"
        price_float = 0

        user: User = await UserDAO.get_one_or_none(chat_id=self.chat_id)

        device.xpath('//*[@resource-id="amount"]').set_text(f"{user.amount}")

        def fnd(element, index: int, array: list, j: int = 0):
            if j > 10:
                return
            limits = device.xpath(
                f"(//android.widget.TextView)[{5+j+index}]"
            ).get_text()
            if not "–" in limits:
                return fnd(element=element, index=index, array=array, j=j + 1)

            print("Element found:", element.get_text())
            for_one = element.get_text()
            username = device.xpath(
                f"(//android.widget.TextView)[{index+j+0}]"
            ).get_text()
            negatiotions = device.xpath(
                f"(//android.widget.TextView)[{1+j+index}]"
            ).get_text()
            method = device.xpath(
                f"(//android.widget.TextView)[{7+j+index}]"
            ).get_text()
            price_str = for_one.replace(",", ".").replace(" ", "")

            pattern = re.compile(r"[+-]?\d+\.?\d*")
            price_re = re.findall(pattern=pattern, string=price_str)[0]
            price_float = float(price_re)
            print(price_float)
            array.append(
                {
                    "for_one": for_one,
                    "username": username,
                    "negatiotions": negatiotions,
                    "limits": limits,
                    "method": method,
                    "price_float": price_float,
                }
            )

        def find(i=0):
            # Поиск элемента по тексту с использованием регулярного выражения
            # pattern = r"\b\d{1,3},\d{2}\s*RUB\b"
            # elements = device.xpath(f'//*[matches(@text, "{pattern}")]').all()

            # for element in elements:
            #     print("Найден элемент с текстом:", element.text)
            elements = device(className="android.widget.TextView")
            array = []
            for index, element in enumerate(elements):
                if (
                    element
                    and "RUB" in element.get_text()
                    and not "–" in element.get_text()
                ):
                    fnd(element=element, index=index, array=array)
                    # print(array[-1])

            # for_one = device.xpath(f"(//android.widget.TextView)[{0+i}]").get_text()
            # username = device.xpath(f"(//android.widget.TextView)[{3+i}]").get_text()
            # negatiotions = device.xpath(
            #     f"(//android.widget.TextView)[{7+i}]"
            # ).get_text()
            # limits = device.xpath(f"(//android.widget.TextView)[{8+i}]").get_text()
            # method = device.xpath(f"(//android.widget.TextView)[{10+i}]").get_text()
            # price_str = for_one.replace(",", ".").replace(" ", "")

            # pattern = re.compile(r"[+-]?\d+\.?\d*")
            # price_re = re.findall(pattern=pattern, string=price_str)[0]
            # price_float = float(price_re)
            # print(price_float)
            # return for_one, username, negatiotions, limits, method, price_float
            return array

        i = 0
        items = 0
        array = []
        while items < 3 and i < 1:
            try:
                array = await asyncio.to_thread(find, i)
                i += 10
                # array.append(
                #     {
                #         "for_one": for_one,
                #         "username": username,
                #         "negatiotions": negatiotions,
                #         "limits": limits,
                #         "method": method,
                #         "price_float": price_float,
                #     }
                # )

                items += 1
            except Exception as e:
                logger.error(f"Ошибка в парсинге {e}")
                i += 1
        lst = self.last.copy()
        self.last = []
        for a in array:
            try:
                logger.debug(f"limits:{a['limits']}")
                limits = a["limits"].split(" – ")
                limit_a_str = limits[0].replace(" ", "").replace(",", ".")
                limit_b_str = limits[1].replace(" ", "").replace(",", ".")

                logger.info(f"limit a {limit_a_str}, limit b {limit_b_str}")
                pattern = re.compile(r"[+-]?\d+\.?\d*")

                limit_a = float(
                    "".join(re.findall(pattern=pattern, string=limit_a_str))
                )
                limit_b = float(
                    "".join(re.findall(pattern=pattern, string=limit_b_str))
                )
            except Exception as e:
                logger.error(f"parse limits {e}")
                raise
            self.last.append(a["price_float"])
            if (
                a["price_float"] <= user.price
                and (len(lst) == 0 or a["price_float"] not in lst)
                and (user.dimension == 0 or user.dimension <= limit_b)
            ):
                logger.info("TRUE")

                await bot.send_message(
                    chat_id=self.chat_id,
                    text=f"Цена за 1: {a['for_one']}\n"
                    f"Имя: {a['username']}\n"
                    f"Кол-во сделок: {a['negatiotions']}\n"
                    f"Лимиты: {a['limits']}\n"
                    f"Способ оплаты: {a['method']}\n",
                )
                logger.info(
                    f"NOTIFY: {a['price_float']} <= {user.price} and ({len(lst)} > 0 and {a['price_float']} not in {lst}) and ({user.dimension} == 0 or {user.dimension} <= {limit_b}) FALSE Цена за 1: {a['for_one']}\n Имя: {a['username']}\nКол-во сделок: {a['negatiotions']}\nЛимиты: {a['limits']}\nСпособ оплаты: {a['method']}\n"
                )
            else:
                logger.debug(
                    f"{a['price_float']} <= {user.price} and ({len(lst)} > 0 and {a['price_float']} not in {lst}) and ({user.dimension} == 0 or {user.dimension} <= {limit_b}) FALSE Цена за 1: {a['for_one']}\n Имя: {a['username']}\nКол-во сделок: {a['negatiotions']}\nЛимиты: {a['limits']}\nСпособ оплаты: {a['method']}\n"
                )
        logger.debug(f"LAST:==========={self.last}")

    async def start_func(self):
        self.running = True

    async def stop_func(self):
        self.running = False

    async def change_price(self, price):
        self.min_price = price

    async def run(self):
        while self.running:
            try:
                await self.p2p_page()
            except Exception as e:
                logger.error(f"run: {e}")
            await asyncio.sleep(0.1)
