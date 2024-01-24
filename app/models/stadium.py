from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class StadiumModel(Base):
    __tablename__ = "stadiums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    price = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UsersModel", back_populates="stadiums")

    booking = relationship("BookingModel", back_populates="stadium")

