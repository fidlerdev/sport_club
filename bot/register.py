from datetime import date
from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Cancel, Calendar
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from loguru import logger

from bot.state import RegisterSG
from database import query
from database.enums import Role


async def on_full_name(msg: types.Message, input: ManagedTextInput, manager: DialogManager, *args) -> None:
    manager.dialog_data["full_name"] = msg.text
    await manager.switch_to(RegisterSG.phone)


async def on_phone(msg: types.Message, input: ManagedTextInput, manager: DialogManager, *args) -> None:
    manager.dialog_data["phone"] = msg.text
    await manager.switch_to(RegisterSG.birthday)


async def on_date_selected(callback: types.CallbackQuery, widget,
                        manager: DialogManager, selected_date: date):
    items = list(manager.dialog_data.items())
    items.append(("birthday", selected_date))

    for k, v in items:
        logger.debug(f"{k = } {v = }")
        query.update_user_info(
            callback.from_user.id,
            k,
            v
        )
    query.update_user_role(callback.from_user.id, Role.MEMBER)
    await callback.message.answer("Вы зарегистрированы! Можете воспользоваться личным кабинетом /account")
    await manager.done()

dialog = Dialog(

    Window(
        Const("Введите полное имя:"),
        TextInput(
            id="__1",
            on_success=on_full_name,
        ),
        Cancel(Const("Отмена")),
        state=RegisterSG.full_name,
    ),

    Window(
        Const("Введите номер телефона:"),
        TextInput(
            id="__2",
            on_success=on_phone
        ),
        Cancel(Const("Отмена")),
        state=RegisterSG.phone,
    ),

    Window(
        Const("Выберите дату рождения:"),
        Calendar(
            id="__3",
            on_click=on_date_selected,
        ),
        Cancel(Const("Отмена")),
        state=RegisterSG.birthday,
    ),

)
