import operator
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select, Start
from aiogram import F
from aiogram.dispatcher.middlewares.user_context import EventContext
from loguru import logger

from bot.state import TrainingListSG
from database import query
from database.enums import Role


async def training_list_getter(
    dialog_manager: DialogManager,
    event_context: EventContext,
    **kwargs: dict
) -> dict:
    logger.debug(f"{kwargs = }")
    logger.debug(f"{dialog_manager.start_data = }")
    role: F = dialog_manager.start_data["role"]

    if role & Role.MEMBER:
        return {"trainings": query.get_member_trainings(event_context.user.id)
                }
    if role & Role.TRAINER:
        return {"trainings": query.get_trainer_trainings(event_context.user.id)
                }
    if role & Role.ADMIN:
        return {"trainings": query.get_all_trainings(event_context.user.id)
                }


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
        # Start(
        #     Const("Назначить тренировку"),
        #     state=
        #     id="__s_create_training",
        #     data=F["role"],
        # ),
        Cancel(Const("Назад")),
        state=TrainingListSG.main,
        getter=training_list_getter,
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
