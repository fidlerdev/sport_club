from aiogram import Router, types, F
from aiogram.filters import BaseFilter, Command, CommandStart
from aiogram_dialog import DialogManager

from database import query

from bot.state import BotSG, RegisterSG, UserAccountSG
from database.enums import Role


handler_router = Router()

class NotUndefinedFilter(BaseFilter):

    async def __call__(self, message: types.Message) -> bool:
        return query.get_user_role(message.from_user.id) != Role.UNDEFINED


@handler_router.message(CommandStart())
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
        await dialog_manager.start(UserAccountSG.main, data={"user_id": user_id, "role": query.get_user_role(user_id)})
    

@handler_router.message(Command("account"), NotUndefinedFilter())
async def on_account(msg: types.Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(BotSG.account, data={"user_id": msg.from_user.id, "role": query.get_user_role(msg.from_user.id)})
