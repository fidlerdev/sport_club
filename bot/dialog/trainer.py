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
        Cancel(Const("Назад")),
        state=TrainerAccountSG.members,
        preview_data={
            "members": [
                [1, "Иванов", "Иван"],
                [2, "Петров", "Петр"],
                [3, "Сидоров", "Сидор"],
                [4, "Кузнецов", "Кузьма"],
                [5, "Михайлов", "Михаил"],
                [6, "Лебедев", "Леонид"],
                [7, "Николаев", "Николай"],
                [8, "Орлов", "Орлан"],
                [9, "Павлов", "Павел"],
                [10, "Семенов", "Семен"],
                [11, "Тихонов", "Тихон"],
                [12, "Чернов", "Чернобай"],
            ]
        }
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
        Cancel(Const("Назад")),
        state=TrainerAccountSG.create_training,
        preview_data={
            "client_name": "Иванов Иван",
            "date_time": "12.12.2024 08:00",
            "intensity": "Высокая",
            "description": "",
        }
    ),
    
 )
