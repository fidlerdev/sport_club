from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import config

from aiogram_dialog.tools import render_preview

from .dialog import member_dialog


bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


dp = Dispatcher(storage=MemoryStorage())


async def start_bot():
    dp.include_routers(member_dialog)
    await render_preview(dp, "render.html")
    
