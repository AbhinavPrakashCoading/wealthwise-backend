from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..core.db import get_db
from ..schemas.schemas import IntegrationConnectRequest
from ..models.models import IntegrationToken, User
from ..auth.security import get_current_user

router = APIRouter(prefix="/integrations", tags=["integrations"])

@router.post("/connect")
def connect(payload: IntegrationConnectRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Placeholder: store a fake token as if OAuth/AA succeeded
    token = IntegrationToken(
        user_id=user.id,
        provider=payload.provider,
        access_token=f"{payload.provider}_access_{datetime.utcnow().timestamp()}",
        refresh_token=f"{payload.provider}_refresh",
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(token)
    db.commit()
    return {"status": "connected", "provider": payload.provider}

@router.get("/tokens")
def list_tokens(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tokens = db.query(IntegrationToken).filter(IntegrationToken.user_id == user.id).all()
    return [{"provider": t.provider, "expires_at": t.expires_at.isoformat()} for t in tokens]
