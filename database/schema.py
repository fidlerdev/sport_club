from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .database import Base


class MemberDB(Base):
    __tablename__ = "member"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    birthday: Mapped[datetime]
    phone: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)


class MemberBanDB(Base):
    __tablename__ = "member_ban"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reason: Mapped[str]
    expiration_date: Mapped[datetime]

    member_id: Mapped[int] = mapped_column(ForeignKey("member.id", ondelete="CASCADE"))


class MemberToMembershipDB(Base):
    __tablename__ = "member_to_membership"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    expiration_date: Mapped[datetime]

    member_id = mapped_column(ForeignKey("member.id", ondelete="CASCADE"))
    membership_id = mapped_column(ForeignKey("membership.id"))


class MembershipDB(Base):
    __tablename__ = "membership"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    level: Mapped[int]
    days: Mapped[int]
    price: Mapped[int]


class MembershipLevelDB(Base):
    __tablename__ = "membership_level"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    value: Mapped[int] = mapped_column(unique=True)


class StaffDB(Base):
    __tablename__ = "staff"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    surname: Mapped[str]
    phone: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("staff_role.id", ondelete="SET NULL"))


class StaffRoleDB(Base):
    __tablename__ = "staff_role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    value: Mapped[int] = mapped_column(unique=True)


class TrainerToMemberDB(Base):
    __tablename__ = "trainer_to_member"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id", ondelete="CASCADE"))
    trainer_id: Mapped[int] = mapped_column(ForeignKey("staff.id", ondelete="CASCADE"))


class TrainingDB(Base):
    __tablename__ = "training"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scheduled_datetime: Mapped[datetime]
    intensite: Mapped[str]
    # В минутах
    duration: Mapped[int]
    description: Mapped[str]
    finished: Mapped[bool] = mapped_column(default=True)

    trainer_to_member_id: Mapped[int] = mapped_column(ForeignKey("trainer_to_member.id", ondelete="CASCADE"))
