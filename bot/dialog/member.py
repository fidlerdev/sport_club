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
        Cancel(Const("Приобрести членство")),
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
