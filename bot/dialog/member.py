import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import MemberAccountSG


dialog = Dialog(

    Window(
        Const("<b>Личный кабинет</b>"),
        Format("<b>Имя:</b> {name}"),
        Format("<b>Фамилия:</b> {surname}"),
        Format("<b>Дата рождения:</b> {birthday}"),
        Format("<b>Членство:</b> \"{membership_name}\" до {expiration_date}"),
        SwitchTo(
            Const("Приобрести членство"),
            id="__btn_buy_membership",
            state=MemberAccountSG.membership_list
        ),
        Button(
            Const("Отказаться от членства"),
            id="__btn_cancel_membership",
        ),
        SwitchTo(
            Const("Расписание тренировок"),
            id="__btn_schedule",
            state=MemberAccountSG.trainigs
        ),
        Cancel(Const("Закрыть")),
        state=MemberAccountSG.main,
        preview_data={
            "name": "Иван",
            "surname": "Иванов",
            "membership_name": "VIP",
            "expiration_date": "31.12.2022",
            "birthday": "01.01.1980",
        },
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
        preview_data={
            "memberships": [
                (1, "VIP", 500, 120),
                (2, "Премиум", 1000, 365),
                (3, "VIP+", 1500, 60),
                (4, "VIP++", 2000, 90),
                (5, "VIP+++", 2500, 120),
                (6, "VIP++++", 3000, 30),
                (7, "VIP+++++", 3500, 7),
                (8, "VIP++++++", 4000, 14),
                (9, "VIP+++++++", 4500, 14),
                (10, "VIP++++++++", 5000, 14),
            ]
        },
        state=MemberAccountSG.membership_list,
    ),
    
    Window(
        Const("Расписание тренировок"),
        ScrollingGroup(
            Select(
                Format("{item[1]} | Интенсивность - {item[2]}"),
                id="__select_training",
                item_id_getter=operator.itemgetter(0),
                items="trainings",
            ),
            id="__sg_trainings",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        Cancel(Const("Назад")),
        state=MemberAccountSG.trainigs,
        preview_data={
            "trainings": [
                (1, "12.12.2024 08:00", "Высокая"),
                (2, "15.12.2024 14:00", "Низкая"),
                (3, "18.12.2024 11:00", "Средняя"),
                (4, "21.12.2024 18:00", "Высокая"),
            ]
        },
    ),

)
