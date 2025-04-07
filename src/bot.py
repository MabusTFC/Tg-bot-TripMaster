import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiohttp import web
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from handlers.benefit_rout import (
    node_rout_handler,
    chose_days_zveno_handler,
)

from handlers.create_rout import (
    calendar_handler,
    trip_handler,
)

from handlers.admin_hand import (
    admin_handler,
    manager_handler,
)

from handlers.hands_input import (
    hands_input_handler,
    #change_days_handler,
    #chose_days_handler,
    select_city_handler,
    work_calendar_handler
)
from database.database import init_db

from handlers.greeting_ import (
    auth_handler,
    manual_handler,
    support_handler,
    google_calendar_handler,
    balance_handler,
    saved_routes_handler,
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
    dp.include_router(auth_handler.router)
    dp.include_router(manual_handler.router)
    dp.include_router(support_handler.router)
    dp.include_router(trip_handler.router)
    dp.include_router(hands_input_handler.router)
    dp.include_router(calendar_handler.router)
    dp.include_router(select_city_handler.router)
    #dp.include_router(change_days_handler.router)
    #dp.include_router(chose_days_handler.router)
    dp.include_router(node_rout_handler.router)
    dp.include_router(work_calendar_handler.router)
    dp.include_router(google_calendar_handler.router)
    dp.include_router(balance_handler.router)
    dp.include_router(saved_routes_handler.router)
    dp.include_router(admin_handler.router)
    dp.include_router(manager_handler.router)
    dp.include_router(chose_days_zveno_handler.router)
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