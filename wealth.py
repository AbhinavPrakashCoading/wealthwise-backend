from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ..core.db import get_db
from ..models.models import Holding, User
from ..schemas.schemas import WealthSummary, HoldingOut
from ..auth.security import get_current_user

router = APIRouter(prefix="/wealth", tags=["wealth"])

@router.get("/holdings", response_model=List[HoldingOut])
def list_holdings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    hs = db.query(Holding).filter(Holding.user_id == user.id).all()
    return hs

@router.get("/summary", response_model=WealthSummary)
def summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    hs = db.query(Holding).filter(Holding.user_id == user.id).all()
    totals: Dict[str, float] = {"stock": 0.0, "mutual_fund": 0.0, "bank": 0.0, "fd": 0.0}
    for h in hs:
        totals[h.type] = totals.get(h.type, 0.0) + (h.value if h.value else 0.0)
    return {"totals": {k: round(v, 2) for k, v in totals.items()}, "holdings": hs}
