from aiogram import Dispatcher, Bot, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.input_data_dialog import input_data_dialog
import config

from aiogram_dialog import setup_dialogs
from database.enums import Role

from .register import dialog as register_dialog
from .handler import handler_router

from .root_dialog import root_dialog

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher(storage=MemoryStorage())
setup_dialogs(dp)


async def start_bot():
    dp.include_routers(
        root_dialog,
        handler_router,
        register_dialog,
        input_data_dialog,
    )

    # await render_preview(dp, "render.html")

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([
        types.BotCommand(command="account", description="Личный кабинет"),
        types.BotCommand(command="set_member", description=f"Изменить роль на: {Role.MEMBER.name}"),
        types.BotCommand(command="set_trainer", description=f"Изменить роль на: {Role.TRAINER.name}"),
        types.BotCommand(command="set_admin", description=f"Изменить роль на: {Role.ADMIN.name}"),
    ])
    await dp.start_polling(bot)
