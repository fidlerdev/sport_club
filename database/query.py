from typing import Any
from sqlalchemy import insert, select, delete, update

from .database import engine, Base, session_factory
from .schema import UserDB, UserRoleDB
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