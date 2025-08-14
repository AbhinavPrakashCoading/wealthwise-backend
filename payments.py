from fastapi import APIRouter, Depends
from urllib.parse import urlencode
from ..schemas.schemas import UpiLinkRequest
from ..auth.security import get_current_user
from ..models.models import User

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/upi-link")
def upi_link(req: UpiLinkRequest, user: User = Depends(get_current_user)):
    params = {
        "pa": req.payee_vpa,
        "pn": req.payee_name,
        "am": f"{req.amount:.2f}",
        "tn": req.note or "WealthWise settlement",
        "cu": "INR",
    }
    return {"link": "upi://pay?" + urlencode(params)}
