from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from ..core.db import get_db
from ..models.models import Group, GroupMember, Expense, ExpenseSplit, Settlement, User
from ..schemas.schemas import GroupCreate, GroupOut, ExpenseCreate, ExpenseOut, SettlementCreate, BalanceItem
from ..auth.security import get_current_user

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=GroupOut)
def create_group(payload: GroupCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    group = Group(name=payload.name)
    db.add(group)
    db.flush()
    # ensure creator is member
    db.add(GroupMember(group_id=group.id, user_id=user.id))
    for uid in set(payload.member_ids or []):
        if uid != user.id:
            db.add(GroupMember(group_id=group.id, user_id=uid))
    db.commit()
    db.refresh(group)
    return group

@router.get("/", response_model=List[GroupOut])
def list_groups(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    groups = db.query(Group).join(GroupMember).filter(GroupMember.user_id == user.id).all()
    return groups

@router.get("/{group_id}", response_model=GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    # membership check
    member = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member")
    return group

@router.post("/{group_id}/expenses", response_model=ExpenseOut)
def add_expense(group_id: int, expense_in: ExpenseCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # membership check
    member = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member")
    total_split = sum(s.amount for s in expense_in.splits)
    if round(total_split, 2) != round(expense_in.amount, 2):
        raise HTTPException(status_code=400, detail="Splits must sum to amount")
    expense = Expense(group_id=group_id, payer_id=expense_in.payer_id, amount=expense_in.amount, description=expense_in.description)
    db.add(expense)
    db.flush()
    for s in expense_in.splits:
        db.add(ExpenseSplit(expense_id=expense.id, user_id=s.user_id, amount=s.amount))
    db.commit()
    db.refresh(expense)
    return expense

@router.get("/{group_id}/balances", response_model=List[BalanceItem])
def get_balances(group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Ensure membership
    member = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member")
    # Initialize nets
    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    nets: Dict[int, float] = {m.user_id: 0.0 for m in members}
    # Expenses: each split adds -amount to that user; payer gets +amount of each split
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    for e in expenses:
        splits = db.query(ExpenseSplit).filter(ExpenseSplit.expense_id == e.id).all()
        for s in splits:
            nets[s.user_id] -= s.amount
            nets[e.payer_id] += s.amount
    # Settlements
    settlements = db.query(Settlement).filter(Settlement.group_id == group_id).all()
    for st in settlements:
        nets[st.from_user_id] += -st.amount
        nets[st.to_user_id] += st.amount
    return [BalanceItem(user_id=uid, net=round(val, 2)) for uid, val in nets.items()]

@router.post("/{group_id}/settlements")
def add_settlement(group_id: int, payload: SettlementCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # membership check
    member = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member")
    st = Settlement(group_id=group_id, from_user_id=payload.from_user_id, to_user_id=payload.to_user_id, amount=payload.amount, note=payload.note)
    db.add(st)
    db.commit()
    return {"status": "ok", "id": st.id}
