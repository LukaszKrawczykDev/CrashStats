import os, datetime
from jose import jwt, JWTError
from passlib.hash import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal
from app.models.user import User

JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_ALGO   = os.getenv("JWT_ALGO",   "HS256")
EXP_MIN    = int(os.getenv("JWT_EXP_MIN", "60"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_pw(pw: str) -> str:
    return bcrypt.hash(pw)

def verify_pw(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)

def create_access_token(sub: dict) -> str:
    to_encode = {
        **sub,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=EXP_MIN),
    }
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGO)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id: int = payload.get("id")
        if user_id is None:
            raise cred_exc
    except JWTError:
        raise cred_exc

    db = SessionLocal()
    user = db.query(User).get(user_id)
    db.close()
    if user is None:
        raise cred_exc
    return user

def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return user