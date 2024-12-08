from aiogram import Router, types
from aiogram.filters.command import Command, CommandStart
from aiogram_dialog import DialogManager

from database import query

from bot.state import RegisterSG, UserAccountSG
from database.enums import Role


unreg_router = Router()



@unreg_router.message(CommandStart())
async def on_first_start(msg: types.Message, dialog_manager: DialogManager) -> None:
    user_id = msg.from_user.id
    user_db = query.get_user(user_id)
    if not user_db or (query.get_user_role(user_id) == Role.UNDEFINED):
        if not user_db:
            query.add_user(user_id)
        await msg.answer("Вас приветствует спортивный клуб <b>\"GOLD\"</b>. Для начала пройдите регистрацию.")
        await dialog_manager.start(RegisterSG.full_name)
    else:
        await msg.reply("Приветствуем вас в личном кабинете спортивного клуба <b>\"GOLD\"</b>.")
        await dialog_manager.start_dialog(UserAccountSG)
    