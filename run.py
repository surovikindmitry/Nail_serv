import asyncio
from aiogram import Bot, Dispatcher

from app.database.models import async_main
from app.user import router
from config import TOKEN


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass



#нужно установить greenlet