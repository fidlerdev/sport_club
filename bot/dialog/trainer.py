import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import TrainerAccountSG

dialog = Dialog(

    Window(
        Const("<b>Личный кабинет тренера</b>"),
        Format("<b>Имя:</b> {name}"),
        Format("<b>Фамилия:</b> {surname}"),
        Cancel(Const("Клиенты")),
        Cancel(Const("Закрыть")),
        state=TrainerAccountSG.main,
        preview_data={
            "name": "Василий",
            "surname": "Иванов",
        }
    ), 

    
 )
