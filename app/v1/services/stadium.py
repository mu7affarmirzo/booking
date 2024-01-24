from fastapi import HTTPException

from app.models.crud.stadium import add_stadium, get_stadiums, get_stadium_by_id, update_stadium, delete_std


def get_all_stadiums_srv(db, starts_at, ends_at, radius, lang, lat):
    if starts_at and ends_at:

        bookings = get_stadiums(db, starts_at, ends_at)
    elif lang and lat:
        bookings = get_stadiums(db, radius=radius, lang=lang, lat=lat)
    return bookings


def get_stadium_srv(db, std_id):
    bookings = get_stadium_by_id(db, std_id)
    return bookings


def add_stadium_srv(db, owner, stadium):
    std = add_stadium(
        db=db, owner=owner, name=stadium.name, description=stadium.description,
        price=stadium.price, latitude=stadium.latitude, longitude=stadium.longitude
    )
    return std


def update_stadium_srv(db, std_id, owner, std):
    if not owner.is_admin:
        target_std = get_stadium_by_id(db, std_id)
        if target_std.owner == owner:
            target_std = update_stadium(db, std_id, std.dict(exclude_unset=True))
            return target_std
        else:
            raise HTTPException(status_code=401, detail="You do not have the authority over it!")
    else:
        target_std = update_stadium(db, std_id, std.dict(exclude_unset=True))
        return target_std


def delete_std_srv(db, user, std_id):
    if user.is_admin:
        delete_std(db, std_id)
    else:
        booking = get_stadium_by_id(db, std_id)
        if booking and booking.requestor == user:
            delete_std(db, std_id)
        else:
            raise HTTPException(status_code=400)