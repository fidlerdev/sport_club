from datetime import date, datetime
from typing import Any
from loguru import logger
from sqlalchemy import insert, select, delete, update

from .database import engine, Base, session_factory
from .schema import MembershipDB, MemberToMembershipDB, UserDB, UserRoleDB, TrainerToMemberDB, TrainingDB
from .enums import Role


def create_tables():
    Base.metadata.create_all(bind=engine)
    fill_db_roles()

def drop_tables():
    Base.metadata.drop_all(bind=engine)


def get_all_roles() -> list[str]:
    with session_factory() as s:
        query = select(
            UserRoleDB.name
        ).distinct()
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
        query = select(
            UserDB
        ).where(
            UserDB.id== user_id
        )
        return s.execute(query).scalar()


def add_user(user_id: int) -> UserDB:
    with session_factory() as s:
        undef_role = s.execute(select(UserRoleDB).where(UserRoleDB.name == Role.UNDEFINED.name)).scalar_one()
        user = UserDB(id=user_id, role_id=undef_role.id)
        s.add(user)
        s.commit()
        s.refresh(user)
        return user
    
def get_role_id(role: Role) -> int:
    with session_factory() as s:
        return s.execute(select(UserRoleDB.id).where(UserRoleDB.name == role.name)).scalar()

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
                select(
                    UserRoleDB.value
                ).where(
                    UserRoleDB.id == user.role_id
                )
            ).scalar()
            return role_value
        else:
            raise ValueError("User not found")

def get_member_trainings(member_id: int) -> list[TrainingDB]:
    with session_factory() as s:
        users_trainers: list[TrainerToMemberDB] = s.execute(
            select(TrainerToMemberDB)
            .where(TrainerToMemberDB.member_id == member_id)
        ).scalars().all()
        user_trainings: list[TrainingDB] = []
        for inst in users_trainers:
            user_trainings.extend(s.execute(
                select(TrainingDB)
                .where(TrainingDB.trainer_to_member_id == inst.id)
            ).scalars().all())
        
        return user_trainings
            
        
def get_membership_expiration_date(member_id: int) -> date | None:
    with session_factory() as s:
        membership = s.execute(
            select(
                MemberToMembershipDB.expiration_date
            ).where(
                MemberToMembershipDB.member_id == member_id
            ).join(
                MemberToMembershipDB
            )
        ).scalar()
        return membership.expiration_date if membership else None


def get_membership(member_id: int) -> tuple[int, datetime, str] | None:
    with session_factory() as s:
        query = select(
            MembershipDB.id,
            MemberToMembershipDB.expiration_date,
            MembershipDB.name
        ).where(
            MemberToMembershipDB.member_id == member_id
        ).join(
            MembershipDB, MemberToMembershipDB.membership_id == MembershipDB.id
        )
    membership: tuple[datetime, MembershipDB] = s.execute(query).first()
    return membership