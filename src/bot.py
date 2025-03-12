import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiohttp import web
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from handlers import (
    ###
    #
    # Подключение хендлеров
    #
    # ###

)

from config import (
    BOT_TOKEN,
    WEB_HOOK_URL,
    WEB_HOOK_PATH,
    WEB_SERVER_HOST
)


logging.basicConfig(level=logging.INFO)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{WEB_HOOK_URL}{WEB_HOOK_PATH}")


async def main():
    #await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    ###
    #регистрация хендлеров
    # dp.include_router(Название хендлера.router)
    #
    #
    # ###
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_requests_handler.register(app, path=WEB_HOOK_PATH)
    setup_application(app, dp, bot=bot)
    await web._run_app(app, host=WEB_SERVER_HOST)

if __name__ == "__main__":
    asyncio.run(main())