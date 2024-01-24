from decouple import config
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from jose import jwt

from app.core.security import get_password_hash
from app.models.users import UsersModel, TokenModel
from app.v1.schemas.auth import UserCreate
from datetime import datetime


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def update_psw(db: Session, user: UsersModel, psw):
    user = get_user_by_phone_number(db, user.phone_number)

    user.password = get_password_hash(psw)
    db.commit()
    db.refresh(user)


def create_user(db: Session, user: UserCreate):
    db_user = UsersModel(phone_number=user.phone_number,
                         full_name=user.full_name, password=get_password_hash(user.psw))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token({"message": "a new user", "phone number": user.phone_number})
    token = TokenModel(key=token)
    token.owner = db_user
    db.add(token)
    db.commit()
    db.refresh(token)

    return db_user


def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(UsersModel).filter(UsersModel.phone_number == phone_number).first()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_access_token(db: Session, user: UsersModel):
    return db.query(TokenModel).filter(TokenModel.owner == user).first()
