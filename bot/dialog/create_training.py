import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import CreateTrainingSG


dialog = Dialog(
    
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
        state=CreateTrainingSG.main,
        preview_data={
            "client_name": "Иванов Иван",
            "date_time": "12.12.2024 08:00",
            "intensity": "Высокая",
            "description": "",
        }
    ),
    
)
