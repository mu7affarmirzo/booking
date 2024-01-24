from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True, unique=True)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)

    requester_id = Column(Integer, ForeignKey("users.id"))
    requester = relationship("UsersModel", back_populates="bookings")

    stadium_id = Column(Integer, ForeignKey("stadiums.id"))
    stadium = relationship("StadiumModel", back_populates="booking", primaryjoin="BookingModel.stadium_id == StadiumModel.id")

