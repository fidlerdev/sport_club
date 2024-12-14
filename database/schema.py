from datetime import date, datetime
from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from .database import Base


class UserDB(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    birthday: Mapped[Optional[date]] = mapped_column(nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user_role.id", ondelete="SET NULL"))


class UserRoleDB(Base):
    __tablename__ = "user_role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(300))
    value: Mapped[int] = mapped_column(unique=True)


class UserBanDB(Base):
    __tablename__ = "user_ban"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reason: Mapped[str] = mapped_column(String(300))
    expiration_date: Mapped[datetime]

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))


class MemberToMembershipDB(Base):
    __tablename__ = "member_to_membership"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    expiration_date: Mapped[datetime]

    member_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    membership_id = mapped_column(ForeignKey("membership.id"))


class MembershipDB(Base):
    __tablename__ = "membership"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(String(300))
    level: Mapped[int]
    days: Mapped[int]
    price: Mapped[int]


class MembershipLevelDB(Base):
    __tablename__ = "membership_level"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(300))
    value: Mapped[int] = mapped_column(unique=True)


class TrainerToMemberDB(Base):
    __tablename__ = "trainer_to_member"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    trainer_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))


class TrainingDB(Base):
    __tablename__ = "training"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scheduled_datetime: Mapped[datetime]
    intensite: Mapped[str] = mapped_column(String(300))
    # В минутах
    duration: Mapped[int]
    description: Mapped[str] = mapped_column(String(300))
    finished: Mapped[bool] = mapped_column(default=True)

    trainer_to_member_id: Mapped[int] = mapped_column(ForeignKey("trainer_to_member.id", ondelete="CASCADE"))
