from aiogram.fsm.state import State, StatesGroup


class MemberAccountSG(StatesGroup):
    main = State()
    trainigs = State()


class TrainerAccountSG(StatesGroup):
    main = State()
    members = State()
    create_training = State()


class InputDataSG(StatesGroup):
    text = State()
    date = State()
    enum = State()


class TrainingInfoSG(StatesGroup):
    info = State()


class MembershipSG(StatesGroup):
    main = State()


class TrainingListSG(StatesGroup):
    main = State()


class MembershipListSG(StatesGroup):
    main = State()
