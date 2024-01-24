from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash
from app.models.crud.user import get_user_by_phone_number, create_user, get_access_token
from app.models.users import TokenModel, UsersModel
from app.v1.schemas.auth import UserCreate, LoginForm, User


auth_routers = APIRouter()


@auth_routers.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_phone_number(db, user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    if user.psw != user.verify_psw:
        raise HTTPException(status_code=422)
    return create_user(db, user)


# Token endpoint for user login
@auth_routers.post("/login")
async def login_for_access_token(form_data: LoginForm, db: Session = Depends(get_db)):

    user = get_user_by_phone_number(db, form_data.phone_number)

    if not user:
        raise HTTPException(status_code=404, detail="Incorrect password or phone number")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = get_access_token(db, user)

    return {"access_token": access_token.key, "token_type": "bearer"}
