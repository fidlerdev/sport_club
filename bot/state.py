from aiogram.fsm.state import State, StatesGroup


class MemberAccountSG(StatesGroup):
    main = State()
    membership_list = State()

