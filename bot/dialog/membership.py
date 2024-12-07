import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import MembershipSG


dialog = Dialog(

    Window(
        Const("<b>Информация о тарифе</b>"),
        Format("<b>Название</b>: {name}"),
        Format("<b>Включено: {included} </b>"),
        Format("<b>Описание:</b> {description}"),
        Format("<b>Цена:</b> {price}"),
        Format("<b>Срок действия:</b> {days} дней"),
        Cancel(Const("Назад")),
        state=MembershipSG.main,
        preview_data={
            "name": "VIP+",
            "included": "Тренажерный зал, СПА, диетолог, питание",
            "description": "VIP+ - это наш лучший тариф",
            "price": "1500",
            "days": 7
        }
    ),

)
