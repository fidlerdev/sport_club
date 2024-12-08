import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import UserAccountSG


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
        Cancel(Const("Тренировки")),
        Cancel(Const("Закрыть")),
        state=UserAccountSG.main,
        preview_data={
            "name": "Иван",
            "surname": "Иванов",
            "membership_name": "VIP",
            "expiration_date": "31.12.2022",
            "birthday": "01.01.1980",
        },
    ),

)
