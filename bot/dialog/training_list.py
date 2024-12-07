import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import TrainingListSG

dialog = Dialog(
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
        Cancel(Const("Назначить тренировку")),
        Cancel(Const("Назад")),
        state=TrainingListSG.member_trainings,
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
