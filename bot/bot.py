from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import config

from aiogram_dialog import setup_dialogs
from aiogram_dialog.tools import render_preview

from .dialog import *
from .handler import unreg_router


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
        account_dialog,
        member_list_dialog,
        trainer_dialog,
        training_dialog,
        training_list_dialog,
        create_training_dialog,
        membership_dialog,
        membership_list_dialog,
        unreg_router,
        register_dialog
    )
    
    await render_preview(dp, "render.html")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
