from typing import List

from fastapi import FastAPI, APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_204_NO_CONTENT

from app.core.database import get_db
from app.core.security import authenticate_user
from app.v1.schemas.bookings import BookingsSchema, CreateBookingSchema, UpdateBookingSchema
from app.models.crud.booking import get_all_bookings, get_stadium_owners_bookings, get_booking_by_id
from app.v1.services.bookings import create_booking_srv, delete_booking_srv, update_booking_srv

booking_router = APIRouter()


@booking_router.get("/list", response_model=List[BookingsSchema])
async def bookings_list_view(db: Session = Depends(get_db), user: dict = Depends(authenticate_user)):
    if user.is_admin:
        bookings = get_all_bookings(db)
        return bookings
    else:
        bookings = get_stadium_owners_bookings(db, user)
        return bookings


@booking_router.get("/{booking_id}", response_model=BookingsSchema)
async def get_booking_view(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)
    return booking


@booking_router.post("/add", response_model=BookingsSchema)
async def add_booking_view(booking_data: CreateBookingSchema, db: Session = Depends(get_db),
                           user: dict = Depends(authenticate_user)):
    booking = create_booking_srv(db, user, booking_data)
    return booking


@booking_router.patch("/{booking_id}", response_model=BookingsSchema)
async def update_booking_view(
        booking_id: int, stadium: UpdateBookingSchema,
        db: Session = Depends(get_db), user: dict = Depends(authenticate_user)
):
    std = update_booking_srv(db, booking_id, user, stadium)
    return std


@booking_router.delete("/delete/{booking_id}", response_model=BookingsSchema)
async def del_booking_view(booking_id: int, db: Session = Depends(get_db),
                           user: dict = Depends(authenticate_user)):
    delete_booking_srv(db, user, booking_id)
    return Response(status_code=204)
