from datetime import date, datetime, timedelta
from functools import partial
import operator
from typing import Any
from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Calendar, Row, Button, Cancel, Multiselect, Column, Select
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from loguru import logger
from .state import InputDataSG


async def on_start(data: Any, manager: DialogManager) -> None:
    ...


async def dialog_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    _ = dialog_manager.start_data
    return {
        "label": _["label"],
    }


async def on_text_input(
    msg: types.Message,
    input: ManagedTextInput,
    manager: DialogManager,
    *args
) -> None:
    await manager.done(
        {
            "name": manager.start_data["name"],
            "value": msg.text,
        }
    )


async def date_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {
        "time": dialog_manager.dialog_data.get("time", "10:00"),
    }


async def change_time(
    callback: types.CallbackQuery,
    button: Button,
    manager: DialogManager,
    minutes: int,
    operation: int
) -> None:
    cur_time = manager.dialog_data.get("time", "10:00")
    d = datetime.strptime(cur_time, "%H:%M")
    if operation < 0:
        d = d - timedelta(minutes=minutes)
    else:
        d = d + timedelta(minutes=minutes)
    manager.dialog_data["time"] = d.strftime("%H:%M")


async def on_date(
    callback: types.CallbackQuery, widget,
    manager: DialogManager, selected_date: date
) -> None:
    await manager.done(
        {
            "name": manager.start_data["name"],
            "value": f"{selected_date.strftime(r"%d.%m.%Y")} {manager.dialog_data.get("time", "10:00")}",
        }
    )


async def multi_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> None:
    return {
        "items": dialog_manager.start_data["items"]
    }


async def on_multi_changed(
    event: types.CallbackQuery, select: Select, manager: DialogManager, data: Any
) -> None:
    logger.debug(f"{data = }")
    manager.dialog_data["value"] = manager.dialog_data.get("value", 0) ^ int(data)


async def on_confirm_enum(
    callback: types.CallbackQuery, btn: Button, manager: DialogManager
) -> None:
    await manager.done({"name": manager.start_data["name"], "value": manager.dialog_data.get("value", 0)})


input_data_dialog = Dialog(

    Window(
        Format("{label}"),
        TextInput(
            id="__ti",
            on_success=on_text_input,
        ),
        Cancel(
            Const("Отмена"),
            result={"name": None, "value": None},
        ),
        state=InputDataSG.text
    ),

    Window(
        Format("{label}"),
        Row(
            Button(
                Const("⏪ 1ч"),
                id="__take_1h",
                on_click=partial(change_time, minutes=60, operation=-1),
            ),
            Button(
                Const("⏪ 30м"),
                id="__take_30m",
                on_click=partial(change_time, minutes=30, operation=-1),
            ),
            Button(
                Const("⏪ 10м"),
                id="__take_10m",
                on_click=partial(change_time, minutes=10, operation=-1),
            ),
            Button(
                Format("{time}"),
                id="__bth_time",
            ),
            Button(
                Const("10м ⏩"),
                id="__give_10m",
                on_click=partial(change_time, minutes=10, operation=+1),
            ),
            Button(
                Const("30м ⏩"),
                id="__give_30m",
                on_click=partial(change_time, minutes=30, operation=+1),
            ),
            Button(
                Const("1ч ⏩"),
                id="__give_1h",
                on_click=partial(change_time, minutes=60, operation=+1),
            ),
        ),
        Calendar(
            id="calendar",
            on_click=on_date,
        ),
        Cancel(
            Const("Отмена"),
            result={"name": None, "value": None},
        ),
        state=InputDataSG.date,
        getter=date_getter,
    ),

    Window(
        Format("{label}"),
        Column(
            Multiselect(
                Format("✅ {item[0]}"),
                Format("❌ {item[0]}"),
                id="multiselect",
                item_id_getter=operator.itemgetter(1),
                items="items",
                on_state_changed=on_multi_changed
            ),
            id="__col"
        ),
        Button(
            Const("Подтвердить"),
            id="__confirm_enum",
            on_click=on_confirm_enum,
        ),
        getter=multi_getter,
        state=InputDataSG.enum,
    ),
    getter=dialog_getter,
    on_start=on_start,
)
