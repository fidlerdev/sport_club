from aiogram.fsm.state import State, StatesGroup


class MemberAccountSG(StatesGroup):
    main = State()
    membership_list = State()
    trainigs = State()


class TrainerAccountSG(StatesGroup):
    main = State()
    members = State()
    member_trainings = State()
    create_training = State()


class InputDataSG(StatesGroup):
    text = State()
    date = State()
    enum = State()
    
class TrainingInfoSG(StatesGroup):
    info = State()

class MembershipSG(StatesGroup):
    main = State()