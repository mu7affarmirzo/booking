import random

from fastapi import HTTPException

from app.models import BookingModel, StadiumModel


def get_all_bookings(db):
    bookings = db.query(BookingModel).all()
    return bookings


def get_booking_by_id(db, booking_id):
    bookings = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    return bookings


def get_booking_by_interval(db, booking_id, start_time, end_time):
    bookings = (
        db.query(BookingModel)
        .filter(BookingModel.stadium_id == booking_id, BookingModel.starts_at >= start_time, BookingModel.ends_at <= end_time)
        .all()
    )
    return bookings


def get_stadium_owners_bookings(db, user):
    bookings = (
        db.query(BookingModel)
        .join(StadiumModel, BookingModel.stadium_id == StadiumModel.id)
        .filter(StadiumModel.owner == user)
        .all()
    )
    return bookings


def create_booking(db, requester, booking):
    key = f"{booking.starts_at.date()}-{requester.id}-{booking.stadium_id}-{random.randint(1000, 9999)}"
    db_booking = BookingModel(
        requester=requester, key=key, stadium_id=booking.stadium_id,
        starts_at=booking.starts_at, ends_at=booking.ends_at
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking


def update_booking(db, booking_id, data):
    booking_query = (
        db.query(BookingModel).
        filter(BookingModel.id == booking_id)
    )
    db_booking = booking_query.first()

    if not db_booking:
        raise HTTPException(status_code=404)

    booking_query.filter(BookingModel.id == booking_id).update(
        data,
        synchronize_session=False
    )
    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db, booking_id):
    booking_query = db.query(BookingModel).filter(BookingModel.id == booking_id)
    booking = booking_query.first()
    if not booking:
        raise HTTPException(status_code=404,
                            detail=f'No booking with this id: {id} found')
    booking_query.delete(synchronize_session=False)
    db.commit()
