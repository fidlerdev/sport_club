import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, ScrollingGroup, Select

from bot.state import MembershipListSG

dialog = Dialog(
    Window(
        Const("<b>Список тарифов</b>"),
        ScrollingGroup(
            Select(
                Format("{item[1]} | {item[2]} ₽ | {item[3]} дней"),
                id="__select_membership",
                item_id_getter=operator.itemgetter(0),
                items="memberships",
            ),
            id="__sg_membership",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        Cancel(Const("Назад")),
        preview_data={
            "memberships": [
                (1, "VIP", 500, 120),
                (2, "Премиум", 1000, 365),
                (3, "VIP+", 1500, 60),
                (4, "VIP++", 2000, 90),
                (5, "VIP+++", 2500, 120),
                (6, "VIP++++", 3000, 30),
                (7, "VIP+++++", 3500, 7),
                (8, "VIP++++++", 4000, 14),
                (9, "VIP+++++++", 4500, 14),
                (10, "VIP++++++++", 5000, 14),
            ]
        },
        state=MembershipListSG.main,
    ),
)
