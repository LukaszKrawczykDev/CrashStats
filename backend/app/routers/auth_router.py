# backend/app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import RegisterSchema, UserOut
from app.auth import hash_pw, verify_pw, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------- Rejestracja ----------
@router.post("/register", status_code=201)
def register(payload: RegisterSchema):
    db: Session = SessionLocal()

    # sprawdzamy czy email lub username już istnieją
    exists = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    if exists:
        db.close()
        raise HTTPException(status_code=409, detail="Użytkownik już istnieje")

    user = User(
        username=payload.username,
        email=payload.email,
        password=hash_pw(payload.password),
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"msg": "zarejestrowano"}

# ---------- Logowanie ----------
@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == data.username).first()
    db.close()

    if not user or not verify_pw(data.password, user.password):
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane logowania")

    token = create_access_token({
        "id": user.id,
        "role": "admin" if user.is_admin else "user"
    })
    return {"access_token": token, "token_type": "bearer"}

# ---------- Bieżący użytkownik ----------
@router.get("/me", response_model=UserOut)
def me(curr=Depends(get_current_user)):
    return curr