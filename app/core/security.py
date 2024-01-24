from fastapi import Request, HTTPException
from passlib.context import CryptContext

from app.core.database import SessionLocal
from app.models.users import TokenModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(request: Request):
    key = request.headers.get("Authorization")
    if not key:
        raise HTTPException(status_code=401, detail="Authentication required")

    db = SessionLocal()
    try:
        my_auth_key = db.query(TokenModel).filter(TokenModel.key == key).first()
        if not my_auth_key:
            raise HTTPException(status_code=401, detail="Invalid key")

        return my_auth_key.owner
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

