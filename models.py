from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from ..core.db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, default="")
    upi_id: Mapped[str] = mapped_column(String, default="")  # e.g., name@bank
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    groups = relationship("GroupMember", back_populates="user")

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="group", cascade="all, delete-orphan")

class GroupMember(Base):
    __tablename__ = "group_members"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="groups")

    __table_args__ = (UniqueConstraint('group_id', 'user_id', name='uq_group_user'),)

class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), index=True)
    payer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense", cascade="all, delete-orphan")

class ExpenseSplit(Base):
    __tablename__ = "expense_splits"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Float, nullable=False)  # positive means this user owes this amount for the expense

    expense = relationship("Expense", back_populates="splits")

class Settlement(Base):
    __tablename__ = "settlements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), index=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    note: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class IntegrationToken(Base):
    __tablename__ = "integration_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    provider: Mapped[str] = mapped_column(String)  # 'zerodha' or 'aa'
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str] = mapped_column(Text, default="")
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Holding(Base):
    __tablename__ = "holdings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[str] = mapped_column(String)  # 'stock' | 'mutual_fund' | 'bank' | 'fd'
    name: Mapped[str] = mapped_column(String)
    quantity: Mapped[float] = mapped_column(Float, default=0.0)  # for stocks/mf
    value: Mapped[float] = mapped_column(Float, default=0.0)     # current value / balance
    meta: Mapped[str] = mapped_column(Text, default="{}")        # JSON string for extras
