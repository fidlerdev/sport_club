import operator
from typing import Any
from aiogram import F, types
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select, Start
from loguru import logger

from bot.state import TrainingListSG, UserAccountSG
from database import query
from database.enums import Role


async def on_start(data: dict, manager: DialogManager):
    manager.dialog_data["role"] = data["role"]
    manager.dialog_data["user_id"] = data["user_id"]


async def account_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, Any]:
    user = query.get_user(user_id=dialog_manager.dialog_data["user_id"])
    return {
        "role": dialog_manager.dialog_data["role"],
        "full_name": user.full_name,
        "phone": user.phone
    }


dialog = Dialog(

    Window(
        Const("<b>Личный кабинет</b>"),
        Format("<b>Имя:</b> {full_name}"),
        Format("<b>Телефон:</b> {phone}", when=F["phone"]),
        # Format("<b>Дата рождения:</b> {birthday}"),
        # Format("<b>Членство:</b> \"{membership_name}\" до {expiration_date}"),
        Cancel(
            Const("Приобрести членство"),
            when=F["role"] & Role.MEMBER
        ),
        Button(
            Const("Отказаться от членства"),
            id="__btn_cancel_membership",
            when=F["role"] & Role.MEMBER
        ),
        Start(
            Const("Тренировки"),
            id="__start_training_list",
            state=TrainingListSG.main,
            data={"role": F["role"]},
        ),
        Cancel(Const("Закрыть")),
        state=UserAccountSG.main,
        getter=account_getter,
        preview_data={
            "name": "Иван",
            "surname": "Иванов",
            "membership_name": "VIP",
            "expiration_date": "31.12.2022",
            "birthday": "01.01.1980",
        },
    ),
    
    on_start=on_start

)
