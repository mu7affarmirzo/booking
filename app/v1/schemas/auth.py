from pydantic import BaseModel


class LoginForm(BaseModel):
    phone_number: str
    password: str


class UserCreate(BaseModel):
    phone_number: str
    full_name: str
    psw: str
    verify_psw: str


class User(BaseModel):
    id: int
    phone_number: str
    full_name: str
    is_active: bool
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str

