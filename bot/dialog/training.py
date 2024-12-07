import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import TrainingInfoSG




dialog = Dialog(

    Window(
        Const("<b>Информация о тренировке</b>\n"),
        Format("<b>Дата:</b> {date}"),
        Format("<b>Интенсивность:</b> {intensity}"),
        Format("<b>Описание:</b> {description}"),
        Format("<b>Длительность</b>: {duration}"),
        Format("<b>Тренер</b>: {trainer}"),
        Cancel(Const("Назад")),
        Cancel(Const("Изменить время и дату")),
        Cancel(Const("Изменить описание")),
        Cancel(Const("Изменить интенсивность")),
        Cancel(Const("Удалить тренировку")),
        state=TrainingInfoSG.info,
        preview_data={
            "training_id": 1,
            "date": "12.12.2024 08:00",
            "intensity": "Высокая",
            "description": "Тренировка по высокой интensивности",
            "duration": "1 час",
            "trainer": "Иванов И.И.",
        }
    ),

)


