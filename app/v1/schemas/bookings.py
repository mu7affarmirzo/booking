from datetime import datetime
from pydantic import BaseModel


class BookingsSchema(BaseModel):
    id: int
    key: str
    starts_at: datetime
    ends_at: datetime
    requester_id: int
    stadium_id: int


class CreateBookingSchema(BaseModel):
    starts_at: datetime
    ends_at: datetime
    stadium_id: int

    class Config:
        orm_mode = True


class UpdateBookingSchema(BaseModel):
    key: str
    starts_at: datetime
    ends_at: datetime

    stadium_id: int
    requester_id: int

    class Config:
        orm_mode = True

