from .register import dialog as register_dialog

from .account import dialog as account_dialog
from .member_list import dialog as member_list_dialog

from .trainer import dialog as trainer_dialog

from .training import dialog as training_dialog
from .training_list import dialog as training_list_dialog
from .create_training import dialog as create_training_dialog

from .membership import dialog as membership_dialog
from .membership_list import dialog as membership_list_dialog


__all__ = [
    "register_dialog",
    "account_dialog",
    "member_list_dialog",
    "trainer_dialog",
    "training_dialog",
    "training_list_dialog",
    "create_training_dialog",
    "membership_dialog",
    "membership_list_dialog",
]
