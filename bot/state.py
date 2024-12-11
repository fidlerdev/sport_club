from aiogram.fsm.state import State, StatesGroup


class BotSG(StatesGroup):
    account = State()
    create_training = State()
    training = State()
    training_list = State()
    membership = State()
    membership_list = State()
    create_membership = State()
    member_list = State()
    trainer_list = State()
    
    

class UserAccountSG(StatesGroup):
    main = State()


class TrainerAccountSG(StatesGroup):
    main = State()


class CreateTrainingSG(StatesGroup):
    main = State()


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


class MemberListSG(StatesGroup):
    main = State()

    
class RegisterSG(StatesGroup):
    full_name = State()
    phone = State()
    birthday = State()