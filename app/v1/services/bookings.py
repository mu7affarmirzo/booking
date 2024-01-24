from fastapi import HTTPException

from app.models.crud.booking import get_booking_by_id, get_booking_by_interval, create_booking, delete_booking, update_booking


def create_booking_srv(db, user, booking_data):
    booking = get_booking_by_id(db, booking_data.stadium_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Stadium not found!")
    is_booking_exists = get_booking_by_interval(
        db, booking_data.stadium_id, booking_data.starts_at, booking_data.ends_at
    )
    if is_booking_exists:
        raise HTTPException(status_code=404, detail="Stadium is busy!")
    else:
        booking = create_booking(db, user, booking_data)
        return booking


def update_booking_srv(db, booking_id, user, booking):
    if user.is_admin:
        target_booking = update_booking(db, booking_id, booking.dict(exclude_unset=True))
        return target_booking
    else:
        target_booking = get_booking_by_id(db, booking_id)
        if target_booking.owner == user:
            target_booking = update_booking(db, booking_id, booking.dict(exclude_unset=True))
            return target_booking
        else:
            raise HTTPException(status_code=401, detail="You do not have the authority over it!")


def delete_booking_srv(db, user, booking_id):
    if user.is_admin:
        delete_booking(db, booking_id)
    else:
        booking = get_booking_by_id(db, booking_id)
        if booking and booking.requestor == user:
            delete_booking(db, booking_id)
        else:
            raise HTTPException(status_code=400)
