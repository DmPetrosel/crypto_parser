from app.create_bot import bot, dp
import asyncio

from app.stages.start import init_when_restart, register_handlers_start
from app.db.initdb import AsyncBase
from app.db.initdb import sync_engine

AsyncBase.metadata.create_all(sync_engine)
from app.utils.utils import tasks


async def async_main():
    register_handlers_start(dp)
    try:
        task2 = await init_when_restart()
        task = await dp.start_polling(bot)
        # await asyncio.gather(task2,task )
    except Exception as e:
        print(e)
    finally:
        print("The end.")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
