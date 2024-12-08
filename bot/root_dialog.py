import operator
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select, Start
from aiogram import F, types
from aiogram.dispatcher.middlewares.user_context import EventContext
from loguru import logger

from bot.state import BotSG
from database import query
from database.enums import Role


async def dialog_getter(
    dialog_manager: DialogManager,
    event_context: EventContext,
    **kwargs
) -> dict:
    return {
        "role": dialog_manager.start_data["role"],
        "user_id": dialog_manager.start_data["user_id"]
    }


async def delete_message(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await callback.message.delete()
    
async def account_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    user = query.get_user(user_id=dialog_manager.start_data["user_id"])
    membership = query.get_membership(member_id=dialog_manager.start_data["user_id"])
    if membership:
        return {
            "full_name": user.full_name,
            "birthday": user.birthday.strftime(r"%d.%m.%Y"),
            "phone": user.phone,
            "membership_name": membership[2],
            "expiration_date": membership[1].strftime(r"%d.%m.%Y"),
        }
    return {
        "full_name": user.full_name,
        "birthday": user.birthday.strftime(r"%d.%m.%Y"),
        "phone": user.phone,
    }


async def training_list_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "trainings": []
    }


async def create_training_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "client_name": "dummy",
        "date_time": "dummy",
        "intensity": "dummy",
        "description": "dummy",
    }


async def members_list_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "members": []
    }


async def membership_list_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "memberships": [],
    }


root_dialog = Dialog(

    Window(
        Const("<b>Личный кабинет</b>"),
        Format("<b>Имя:</b> {full_name}"),
        Format("<b>Телефон:</b> {phone}", when=F["phone"]),
        Format("<b>Дата рождения:</b> {birthday}"),
        Format("<b>Тариф:</b> \"{membership_name}\" до {expiration_date}", when=F["role"] & Role.MEMBER),
        SwitchTo(
            Const("Приобрести членство"),
            id="__st_membership_list",
            state=BotSG.membership_list,
            when=((F["role"] & Role.MEMBER) & F["membership"].is_(None)) | F["role"] & Role.ADMIN
        ),
        Button(
            Const("Отказаться от членства"),
            id="__btn_cancel_membership",
            when=(F["role"] & Role.MEMBER) & F["membership"].is_not(None)
        ),
        SwitchTo(
            Const("Тренировки"),
            id="__st_training_list",
            state=BotSG.training_list,
        ),
        SwitchTo(
            Const("Список клиентов"),
            id="__st_members_list",
            state=BotSG.member_list,
            when=(F["role"] & Role.ADMIN) | (F["role"] & Role.TRAINER),
        ),
        Cancel(Const("Закрыть"), on_click=delete_message),
        state=BotSG.account,
        getter=account_getter,
        preview_data={
            "name": "Иван",
            "surname": "Иванов",
            "membership_name": "VIP",
            "expiration_date": "31.12.2022",
            "birthday": "01.01.1980",
        },
    ),

    Window(
        Const("<b>Тренировки</b>"),
        ScrollingGroup(
            Select(
                Format("{item[1]} | Интенсивность - {item[2]}"),
                id="__select_member_training",
                item_id_getter=operator.itemgetter(0),
                items="trainings",
            ),
            id="__sg_membertrainings",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        SwitchTo(
            Const("Назначить тренировку"),
            state=BotSG.create_training,
            id="__s_create_training",
            when=F["role"] & Role.TRAINER | F["role"] & Role.ADMIN,
        ),
        SwitchTo(
            Const("Назад"),
            state=BotSG.account,
            id="__st_account",
        ),
        getter=training_list_getter,
        state=BotSG.training_list,
    ),

    Window(
        Const("<b>Назначение тренировки</b>"),
        Format("<b>Клиент:</b> {client_name}"),
        Format("<b>Дата и время:</b> {date_time}"),
        Format("<b>Интенсивность:</b> {intensity}"),
        Format("<b>Описание:</b> {description}"),
        Cancel(Const("Выбрать время")),
        Cancel(Const("Выбрать интенсивность")),
        Cancel(Const("Добавить описание")),
        SwitchTo(
            Const("Назад"),
            state=BotSG.training_list,
            id="__st_training_list",
        ),
        state=BotSG.create_training,
        getter=create_training_getter,
    ),

    Window(
        Const("<b>Клиенты</b>"),
        ScrollingGroup(
            Select(
                Format("{item[1]} {item[2]}"),
                id="__select_member",
                item_id_getter=operator.itemgetter(0),
                items="members",
            ),
            id="__sg_members",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        SwitchTo(
            Const("Назад"),
            state=BotSG.account,
            id="__st_account",
        ),
        state=BotSG.member_list,
        getter=members_list_getter,
    ),

    Window(
        Const("<b>Список тарифов</b>"),
        ScrollingGroup(
            Select(
                Format("{item[1]} | {item[2]} ₽ | {item[3]} дней"),
                id="__select_membership",
                item_id_getter=operator.itemgetter(0),
                items="memberships",
            ),
            id="__sg_membership",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        Cancel(Const("Назад")),
        state=BotSG.membership_list,
        getter=membership_list_getter,
    ),
    
    Window(
        
    ),
    
    getter=dialog_getter,
)