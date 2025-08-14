from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models.models import User
from ..schemas.schemas import UserCreate, UserOut, Token
from ..auth.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_in.email,
        full_name=user_in.full_name or "",
        upi_id=user_in.upi_id or "",
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(form_data: dict = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm doesn't work nicely in typed clients; accept both
    # but we also accept JSON via Depends() trick (FastAPI handles form automatically if provided)
    username = form_data.get("username") or form_data.get("email")
    password = form_data.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
