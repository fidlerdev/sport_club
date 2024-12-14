from datetime import date, datetime, timedelta
from typing import Any
from loguru import logger
from sqlalchemy import insert, select, delete, update, in

from .database import engine, Base, session_factory
from .schema import (
    MembershipDB,
    MemberToMembershipDB,
    UserDB,
    UserRoleDB,
    TrainerToMemberDB,
    TrainingDB,
)
from .enums import Role


def create_tables():
    Base.metadata.create_all(bind=engine)
    fill_db_roles()


def drop_tables():
    Base.metadata.drop_all(bind=engine)


def get_all_roles() -> list[str]:
    with session_factory() as s:
        query = select(UserRoleDB.name).distinct()
        return s.execute(query).scalars().all()


def fill_db_roles():
    roles = get_all_roles()
    with session_factory() as s:
        for role in Role:
            if role.name in roles:
                continue
            s.add(UserRoleDB(name=role.name, value=role.value))
            s.commit()


def get_user(user_id: int) -> UserDB | None:
    with session_factory() as s:
        query = select(UserDB).where(UserDB.id == user_id)
        return s.execute(query).scalar()


def add_user(user_id: int) -> UserDB:
    with session_factory() as s:
        undef_role = s.execute(
            select(UserRoleDB).where(UserRoleDB.name == Role.UNDEFINED.name)
        ).scalar_one()
        user = UserDB(id=user_id, role_id=undef_role.id)
        s.add(user)
        s.commit()
        s.refresh(user)
        return user


def get_role_id(role: Role) -> int:
    with session_factory() as s:
        return s.execute(
            select(UserRoleDB.id).where(UserRoleDB.name == role.name)
        ).scalar()


def update_user_role(user_id: int, role: Role) -> UserDB:
    with session_factory() as s:
        user = get_user(user_id)
        if user:
            user.role_id = get_role_id(role)
            s.add(user)
            s.commit()
            return user
        else:
            raise ValueError("User not found")


def update_user_info(user_id: int, field: str, value: Any) -> UserDB:
    with session_factory() as s:
        user = get_user(user_id)
        if user:
            setattr(user, field, value)
            s.add(user)
            s.commit()
            return user
        else:
            raise ValueError("User not found")


def get_user_role(user_id: int) -> int:
    with session_factory() as s:
        user = get_user(user_id)
        if user:
            role_value = s.execute(
                select(UserRoleDB.value).where(UserRoleDB.id == user.role_id)
            ).scalar()
            return role_value
        else:
            raise ValueError("User not found")


def get_member_trainings(member_id: int) -> list[TrainingDB]:
    with session_factory() as s:
        users_trainers: list[TrainerToMemberDB] = (
            s.execute(
                select(TrainerToMemberDB).where(
                    TrainerToMemberDB.member_id == member_id
                )
            )
            .scalars()
            .all()
        )
        user_trainings: list[TrainingDB] = []
        for inst in users_trainers:
            user_trainings.extend(
                s.execute(
                    select(TrainingDB).where(TrainingDB.trainer_to_member_id == inst.id)
                )
                .scalars()
                .all()
            )

        return user_trainings


def get_membership_expiration_date(member_id: int) -> date | None:
    with session_factory() as s:
        membership = s.execute(
            select(MemberToMembershipDB.expiration_date)
            .where(MemberToMembershipDB.member_id == member_id)
            .join(MemberToMembershipDB)
        ).scalar()
        return membership.expiration_date if membership else None


def get_membership(membership_id: int) -> MembershipDB:
    with session_factory() as s:
        return s.execute(
            select(MembershipDB).where(MembershipDB.id == membership_id)
        ).scalar()


def get_user_membership(user_id: int) -> tuple[int, datetime, str] | None:
    with session_factory() as s:
        query = (
            select(
                MembershipDB.id, MemberToMembershipDB.expiration_date, MembershipDB.name
            )
            .where(MemberToMembershipDB.member_id == user_id)
            .join(MembershipDB, MemberToMembershipDB.membership_id == MembershipDB.id)
        )
    membership: tuple[datetime, MembershipDB] = s.execute(query).first()
    return membership


def get_memberships() -> list[MembershipDB]:
    with session_factory() as s:
        return s.execute(select(MembershipDB)).scalars().all()


def get_trainers() -> list[UserDB]:
    trainer_role_id = get_role_id(Role.TRAINER)
    with session_factory() as s:
        users = (
            s.execute(select(UserDB).where(UserDB.role_id == trainer_role_id))
            .scalars()
            .all()
        )
        return users


def add_membership(
    name,
    price,
    days,
    description,
    level,
) -> None:
    with session_factory() as s:
        s.add(
            MembershipDB(
                name=name,
                price=price,
                days=days,
                description=description,
                level=level,
            )
        )
        s.commit()


def delete_membership(membership_id: int) -> None:
    with session_factory() as s:
        s.execute(delete(MembershipDB).where(MembershipDB.id == membership_id))
        s.commit()


def enroll_on_membership(user_id: int, membership_id: int) -> None:
    membership = get_membership(membership_id)
    expiration_date = datetime.now().date() + timedelta(days=membership.days)
    with session_factory() as s:
        s.add(
            MemberToMembershipDB(
                member_id=user_id,
                membership_id=membership_id,
                expiration_date=expiration_date,
            )
        )
        s.commit()


def unenroll_membership(user_id: int) -> None:
    with session_factory() as s:
        s.execute(
            delete(MemberToMembershipDB).where(
                MemberToMembershipDB.member_id == user_id
            )
        )
        s.commit()


def get_members() -> list[UserDB]:
    rid = get_role_id(Role.MEMBER)
    with session_factory() as s:
        return s.execute(
            select(UserDB)
            .where(UserDB.role_id == rid)
        ).scalars().all()


def get_user_trainer(member_id: int) -> UserDB | None:
    with session_factory() as s:
        mob_tie = s.execute(
            select(TrainerToMemberDB)
            .where(TrainerToMemberDB.member_id == member_id)
        ).scalar()
        if mob_tie is None:
            return None
        return s.execute(
            select(UserDB)
            .where(UserDB.id == mob_tie.trainer_id)
        ).scalar()


def tie_trainer_and_member(member_id: int, trainer_id: int):
    with session_factory() as s:
        if get_user_trainer(member_id):
            s.execute(
                update(TrainerToMemberDB)
                .values(trainer_id=trainer_id)
                .where(TrainerToMemberDB.member_id == member_id)
            )
            s.commit()
        else:
            s.add(
                TrainerToMemberDB(trainer_id=trainer_id, member_id=member_id)
            )
            s.commit()


def get_user_trainings(user_id: int) -> list[TrainingDB]:
    with session_factory() as s:
        tie = s.execute(
            select(TrainerToMemberDB)
            .where(TrainerToMemberDB.member_id == user_id)
        ).scalar()
        logger.debug(f"{tie =}")
        if not tie:
            return []
        return s.execute(
            select(TrainingDB)
            .where(TrainingDB.trainer_to_member_id == tie.id)
        ).scalars().all()


def get_member_tie(user_id: int):
    with session_factory() as s:
        return s.execute(
            select(TrainerToMemberDB)
            .where(TrainerToMemberDB.member_id == user_id)
        ).scalar()


def get_trainer_trainings(user_id: int) -> list[TrainingDB]:
    with session_factory() as s:
        tie = s.execute(
            select(TrainerToMemberDB)
            .where(TrainerToMemberDB.trainer_id == user_id)
        ).scalar()
        logger.debug(f"{tie =}")
        if not tie:
            return []
        return s.execute(
            select(TrainingDB)
            .where(TrainingDB.trainer_to_member_id == tie.id)
        ).scalars().all()


def add_tie(trainer_id: int, member_id: int):
    with session_factory() as s:
        s.add(
            TrainerToMemberDB(member_id=member_id, trainer_id=trainer_id)
        )
        s.commit()

def add_training(
    tie_id,
    description,
    date_time,
) -> None:
    with session_factory() as s:
        s.add(
            TrainingDB(
                scheduled_datetime=date_time,
                intensite="",
                duration=0,
                description=description,
                trainer_to_member_id=tie_id,
            ),
        )
        s.commit()


def get_training(tr_id: int) -> TrainingDB:
    with session_factory() as s:
        return s.execute(
            select(TrainingDB)
            .where(TrainingDB.id == tr_id)
        ).scalar()

def get_trainer_members(trainer_id: int) -> list[UserDB]:
    with session_factory() as s:
        member_ids = s.execute(
            select(TrainerToMemberDB.member_id)
            .where(TrainerToMemberDB.trainer_id == trainer_id)
        ).scalars().all()
        memebrs: list[UserDB] = s.execute(
            select(UserDB)
            .where(UserDB.id.in_(member_ids))
        ).scalars().all()
        return memebrs
