from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class UsersModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    password = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    activated_at = Column(DateTime, nullable=True)

    token = relationship("TokenModel", back_populates="owner")
    stadiums = relationship("StadiumModel", back_populates="owner")
    bookings = relationship("BookingModel", back_populates="requester")


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UsersModel", back_populates="token")

