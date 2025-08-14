from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: Optional[str] = ""
    upi_id: Optional[str] = ""

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str = ""
    upi_id: str = ""

    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    name: str
    member_ids: List[int] = []

class GroupOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class ExpenseSplitIn(BaseModel):
    user_id: int
    amount: float

class ExpenseCreate(BaseModel):
    payer_id: int
    amount: float
    description: str = ""
    splits: List[ExpenseSplitIn]

class ExpenseOut(BaseModel):
    id: int
    payer_id: int
    amount: float
    description: str
    created_at: datetime
    class Config:
        from_attributes = True

class SettlementCreate(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: float
    note: str = ""

class BalanceItem(BaseModel):
    user_id: int
    net: float  # positive means they should receive, negative means they owe

class HoldingOut(BaseModel):
    id: int
    type: Literal["stock","mutual_fund","bank","fd"]
    name: str
    quantity: float
    value: float
    class Config:
        from_attributes = True

class WealthSummary(BaseModel):
    totals: dict
    holdings: List[HoldingOut]

class IntegrationConnectRequest(BaseModel):
    provider: Literal["zerodha","aa"]
    code: Optional[str] = None  # e.g. OAuth code for zerodha

class UpiLinkRequest(BaseModel):
    payee_vpa: str
    payee_name: str
    amount: float
    note: str = ""
