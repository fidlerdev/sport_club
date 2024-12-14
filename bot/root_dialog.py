import operator
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select, Start
from aiogram import F, types
from aiogram.dispatcher.middlewares.user_context import EventContext
from loguru import logger

from bot.state import BotSG, InputDataSG
from database import query
from database.enums import Role, Level, _l, get_included_string
from datetime import datetime


async def on_member_info(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
    member_id: int
) -> int:
    manager.dialog_data["member_id"] = member_id
    await manager.switch_to(BotSG.member_info)

async def on_select_membership(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
    membership_id: int
) -> None:
    manager.dialog_data["membership_id"] = membership_id
    manager.dialog_data["user_id"] = callback.from_user.id
    await manager.switch_to(BotSG.membership)


async def on_delete_membership(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    query.delete_membership(manager.dialog_data["membership_id"])
    await manager.switch_to(BotSG.membership_list)


async def on_enroll_membership(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    query.enroll_on_membership(callback.from_user.id, manager.dialog_data["membership_id"])
    await manager.switch_to(BotSG.account)


async def on_unenroll_membership(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    query.unenroll_membership(callback.from_user.id)


async def process_input_data(
    start_data: dict, result: dict,
    manager: DialogManager
) -> None:
    manager.dialog_data[result["name"]] = result["value"]


async def dialog_getter(
    dialog_manager: DialogManager,
    event_context: EventContext,
    **kwargs
) -> dict:
    match dialog_manager.start_data["role"]:
        case Role.MEMBER:
            status = "член клуба"
        case Role.TRAINER:
            status = "тренер"
        case Role.ADMIN:
            status = "администратор"
        case _:
            status = "неопределен"

    return {
        "role": dialog_manager.start_data["role"],
        "user_id": dialog_manager.start_data["user_id"],
        "status": status
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
    membership = query.get_user_membership(user_id=dialog_manager.start_data["user_id"])
    trainer = query.get_user_trainer(user.id)
    logger.debug(f"{membership = }")
    if membership:
        return {
            "full_name": user.full_name,
            "birthday": user.birthday.strftime(r"%d.%m.%Y"),
            "phone": user.phone,
            "membership_name": membership[2],
            "expiration_date": membership[1].strftime(r"%d.%m.%Y"),
            "membership": True,
            "trainer": trainer
        }
    return {
        "full_name": user.full_name,
        "birthday": user.birthday.strftime(r"%d.%m.%Y"),
        "phone": user.phone,
        "membership": False
    }


async def training_list_getter(
    dialog_manager: DialogManager,
    event_context,
    **kwargs
) -> dict:
    user_id = event_context.chat.id
    role = query.get_user_role(user_id)
    logger.debug(f"{user_id = } {role = }")
    if role == Role.TRAINER:
        trainings = query.get_trainer_trainings(user_id)
        logger.debug(f"{trainings = }")
        return {"trainings": [(t.id, t.scheduled_datetime.strftime("%d.%m.%Y %H:%M")) for t in trainings]}
    if role == Role.MEMBER:
        trainings = query.get_user_trainings(user_id)
        logger.debug(f"{trainings = }")
        return {"trainings": [(t.id, t.scheduled_datetime.strftime("%d.%m.%Y %H:%M")) for t in trainings]}
    else:
        return {
            "trainings": []
        }


async def training_info_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    training = query.get_training(dialog_manager.dialog_data["training_id"])
    return {
        "date_time": training.scheduled_datetime.strftime("%d.%m.%Y %H:%M"),
        "description": training.description,
    }


async def show_training_info(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
    tr_id: int
) -> None:
    manager.dialog_data["training_id"] = tr_id
    await manager.switch_to(BotSG.training_info)


async def set_training(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    _ = manager.dialog_data
    query.add_training(
        member_id=_["member_id"],
        trainer_id=callback.from_user.id,
        description=_.get("description", ""),
        date_time=datetime.strptime(_["date_time"], "%d.%m.%Y %H:%M"),
    )
    await manager.switch_to(state=BotSG.training_list)


async def create_training_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    _ = dialog_manager.dialog_data
    return {
        "client_name": query.get_user(_["member_id"]).full_name,
        "date_time": _.get("date_time", "не указано"),
        "description": _.get("description", "не указано"),
    }


async def members_list_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "members": query.get_members()
    }


async def membership_list_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "memberships": query.get_memberships(),
    }


async def membership_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    membership = query.get_membership(dialog_manager.dialog_data["membership_id"])
    return {
        "membership": membership,
        "included": get_included_string(membership.level),
    }


async def create_membership_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    _ = dialog_manager.dialog_data
    level = _.get("level", 0)
    if not level:
        included = "не указаны"
    else:
        included = get_included_string(level)
    return {
        "name": _.get("name", "не указано"),
        "included": included,
        "description": _.get("description", "не указано"),
        "days": _.get("days", "не указано"),
        "price": _.get("price", "не указана"),
    }


async def trainer_list_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "trainers": query.get_trainers()
    }


async def show_trainer_info(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
    trainer_id: int,
) -> None:
    manager.dialog_data["trainer_id"] = trainer_id
    await manager.switch_to(BotSG.trainer_info)


async def trainer_info_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    trainer = query.get_user(dialog_manager.dialog_data["trainer_id"])
    return {
        "full_name": trainer.full_name,
        "birthday": trainer.birthday.strftime(r"%d.%m.%Y"),
        "phone": trainer.phone,
    }

async def on_add_membership(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager
) -> None:
    _ = manager.dialog_data
    logger.debug(f"{_ = }")
    name = _.get("name", "")
    price = int(_.get("price", 0))
    days = int(_.get("days", 0))
    description = _.get("description", "")
    level = int(_.get("level", 0))

    query.add_membership(
        name,
        price,
        days,
        description,
        level,
    )
    await manager.switch_to(BotSG.membership_list)

async def member_info_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "member": query.get_user(dialog_manager.dialog_data["member_id"]),
        "trainer": query.get_user_trainer(dialog_manager.dialog_data["member_id"])
    }

async def tie_trainer(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
    trainer_id: int
) -> None:
    query.tie_trainer_and_member(
        member_id=manager.dialog_data["member_id"],
        trainer_id=trainer_id
    )
    await manager.switch_to(BotSG.member_info)



root_dialog = Dialog(

    Window(
        Const("<b>Личный кабинет</b>"),
        Format("<b>Статус</b>: {status}"),
        Format("<b>Имя:</b> {full_name}"),
        Format("<b>Телефон:</b> {phone}", when=F["phone"]),
        Format("<b>Дата рождения:</b> {birthday}"),
        Format("<b>Тариф:</b> \"{membership_name}\" до {expiration_date}", when=F["role"] == Role.MEMBER & F["membership"].is_(True)),
        Format("<b>Тренер:</b> {trainer.full_name}", when=F["trainer"]),
        SwitchTo(
            Case(
                {
                    Role.MEMBER: Const("Приобрести членство"),
                    Role.ADMIN: Const("Список тарифов")
                },
                selector="role"
            ),
            id="__st_membership_list",
            state=BotSG.membership_list,
            when=(F["role"] == Role.MEMBER) | (F["role"] == Role.ADMIN)
        ),
        Button(
            Const("Отказаться от членства"),
            id="__btn_cancel_membership",
            when=(F["role"] == Role.MEMBER) & (F["membership"].is_(True)),
            on_click=on_unenroll_membership
        ),
        SwitchTo(
            Const("Тренировки"),
            id="__st_training_list",
            state=BotSG.training_list,
            when=F["role"] != Role.ADMIN,
        ),
        SwitchTo(
            Const("Список клиентов"),
            id="__st_members_list",
            state=BotSG.member_list,
            when=(F["role"] == Role.ADMIN) | (F["role"] == Role.TRAINER),
        ),
        Cancel(Const("Закрыть"), on_click=delete_message),
        state=BotSG.account,
        getter=account_getter,
    ),

    Window(
        Const("<b>Информация о клиенте</b>"),
        Format("<b>Имя:</b> {member.full_name}"),
        Format("<b>Телефон:</b> {member.phone}", when=F["phone"]),
        Format("<b>Тренер:</b> {trainer.full_name}", when=F["trainer"]),
        Format("<b>Дата рождения:</b> {member.birthday}"),
        SwitchTo(
            Const("Назад"),
            id="__ssst_memberlist",
            state=BotSG.member_list,
        ),
        SwitchTo(
            Const("Назначить тренера"),
            state=BotSG.trainer_list,
            id="__st_trainer_list",
            when=F["role"] == Role.ADMIN,
        ),
        SwitchTo(
            Const("Назначить тренировку"),
            state=BotSG.create_training,
            id="__s_create_training",
            when=F["role"] == Role.TRAINER,
        ),
        SwitchTo(
            Const("Назад"),
            id="__st_member_list",
            state=BotSG.member_list,
        ),
        getter=member_info_getter,
        state=BotSG.member_info,
    ),

    Window(
        Const("<b>Список тренеров</b>"),
        ScrollingGroup(
            Select(
                Format("{item.full_name}"),
                id="__select_trainer",
                item_id_getter=operator.attrgetter("id"),
                items="trainers",
                on_click=tie_trainer,
            ),
            id="__sg_trainer_list",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        SwitchTo(
            Const("Назад"),
            state=BotSG.account,
            id="__st_account",
        ),
        state=BotSG.trainer_list,
        getter=trainer_list_getter,
    ),

    Window(
        Const("<b>Информация о тренере</b>"),
        Format("<b>Имя:</b> {full_name}"),
        Format("<b>Телефон:</b> {phone}", when=F["phone"]),
        Format("<b>Дата рождения:</b> {birthday}"),
        SwitchTo(
            Const("Назад"),
            id="__st_trainer_list",
            state=BotSG.trainer_list,
            when=F["role"] == Role.ADMIN,
        ),
        state=BotSG.trainer_info,
        getter=trainer_info_getter,
    ),

    Window(
        Const("<b>Тренировки</b>"),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                id="__select_member_training",
                item_id_getter=operator.itemgetter(0),
                items="trainings",
                on_click=show_training_info,
            ),
            id="__sg_membertrainings",
            width=1,
            height=10,
            hide_on_single_page=True,
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
        Const("<b>Информация о тренировке</b>"),
        Format("<b>Дата и время:</b> {date_time}"),
        Format("<b>Описание:</b> {description}"),
        SwitchTo(
            Const("Назад"),
            state=BotSG.training_list,
            id="killme",
        ),
        getter=training_info_getter,
        state=BotSG.training_info,
    ),

    Window(
        Const("<b>Назначение тренировки</b>"),
        Format("<b>Клиент:</b> {client_name}"),
        Format("<b>Дата и время:</b> {date_time}"),
        Format("<b>Описание:</b> {description}"),
        Start(
            Const("Выбрать время"),
            state=InputDataSG.date,
            id="__sfdjsfs",
            data={"name": "date_time", "label": "Выберите время"}
        ),
        Start(
            Const("Добавить описание"),
            state=InputDataSG.text,
            id="__dsfjsjklfh12",
            data={"name": "description", "label": "Введите описание"}
        ),
        Button(
            Const("Сохранить"),
            id="__save",
            on_click=set_training,
        ),
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
                Format("{item.full_name}"),
                id="__select_member",
                item_id_getter=operator.attrgetter("id"),
                on_click=on_member_info,
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
                Format("{item.name} | {item.price} ₽ | {item.days} дней"),
                id="__select_membership",
                item_id_getter=operator.attrgetter("id"),
                items="memberships",
                on_click=on_select_membership,
            ),
            id="__sg_membership",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        SwitchTo(
            Const("Добавить тариф"),
            state=BotSG.create_membership,
            id="__st_create_membership",
            when=F["role"] == Role.ADMIN,
        ),
        SwitchTo(
            Const("Назад"),
            state=BotSG.account,
            id="__st_account",
        ),
        state=BotSG.membership_list,
        getter=membership_list_getter,
    ),

    Window(
        Const("<b>Информация о тарифе</b>"),
        Format("<b>Название</b>: {membership.name}"),
        Format("<b>Включено: {included} </b>"),
        Format("<b>Описание:</b> {membership.description}"),
        Format("<b>Цена:</b> {membership.price}"),
        Format("<b>Срок действия:</b> {membership.days} дней"),
        SwitchTo(
            Const("Назад"),
            id="__st_membership_list",
            state=BotSG.membership_list,
        ),
        Button(
            Const("Приобрести"),
            id="__buy_membership",
            on_click=on_enroll_membership,
            when=F["role"] == Role.MEMBER,
        ),
        state=BotSG.membership,
        getter=membership_getter,
    ),

    Window(
        Const("<b>Создание тарифа</b>"),
        Format("<b>Название</b>: {name}"),
        Format("<b>Описание</b>: {description}"),
        Format("<b>Включенные услуги</b>: {included}"),
        Format("<b>Количество дней</b>: {days}"),
        Format("<b>Цена</b>: {price}"),
        Start(
            Const("Изменить название"),
            id="__change_name_1",
            data={"name": "name", "label": "Введите название тарифа"},
            state=InputDataSG.text
        ),
        Start(
            Const("Изменить описание"),
            id="__change_desc_1",
            data={"name": "description", "label": "Введите описание"},
            state=InputDataSG.text
        ),
        Start(
            Const("Включить услуги"),
            id="__change_level_1",
            data={
                "name": "level",
                "label": "Выберите включенные услуги",
                "items": (
                    (_l[Level.TRAINER], Level.TRAINER),
                    (_l[Level.SWIMMING_POOL], Level.SWIMMING_POOL),
                    (_l[Level.KIDS], Level.KIDS),
                    (_l[Level.DIETOLOG], Level.DIETOLOG),
                    (_l[Level.SPA], Level.SPA),
                    (_l[Level.MEALS], Level.MEALS),
                )
            },
            state=InputDataSG.enum
        ),
        Start(
            Const("Изменить количество дней"),
            id="__change_days_1",
            data={"name": "days", "label": "Введите количество дней"},
            state=InputDataSG.text
        ),
        Start(
            Const("Изменить цену"),
            id="__change_price_1",
            data={"name": "price", "label": "Введите цену"},
            state=InputDataSG.text
        ),
        Button(Const("Добавить"), id="__add_membership", on_click=on_add_membership),
        SwitchTo(
            Const("Назад"),
            state=BotSG.membership_list,
            id="__st_membership_list",
        ),
        state=BotSG.create_membership,
        getter=create_membership_getter,
    ),

    on_process_result=process_input_data,
    getter=dialog_getter,
)
