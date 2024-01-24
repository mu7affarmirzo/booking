from typing import Optional
from math import radians, sin, cos, sqrt, atan2

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import BookingModel
from app.models.stadium import StadiumModel
from geopy import distance


# """
# Haversine oraligi
#
# berilgan kordinatalar orasidagi masofani topish
# """
#
#
# def haversine_distance(lat1, lan1, lat2, lan2):
#     R = 6371
#     print(lat1, lan1)
#     dlat = radians(lat2 - lat1)
#     dlan = radians(lan2 - lan1)
#
#     a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlan / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#     distance = R * c
#     return distance


def get_stadiums(db: Session, starts_at=None, ends_at=None, radius=None, lang=None, lat=None):
    if starts_at and ends_at:
        return (
            db.query(StadiumModel)
            .filter(~StadiumModel.bookings.any(
                BookingModel.starts_at <= ends_at,
                BookingModel.ends_at >= starts_at
            ))
            .all()
        )
    if lang and lat:
        stds = db.query(StadiumModel).all()
        nearby_stadiums = [
            std
            for std in stds
            if distance.distance((lat, lang), (std.latitude, std.longitude)).kilometers < radius
        ]
        return nearby_stadiums

    if starts_at and ends_at and lang and lat:
        stds = db.query(StadiumModel)\
            .filter(~StadiumModel.bookings.any(
                BookingModel.starts_at <= ends_at,
                BookingModel.ends_at >= starts_at
            ))\
            .all()
        nearby_stadiums = [
            std
            for std in stds
            if distance.distance((lat, lang), (std.latitude, std.longitude)).kilometers < radius
        ]
        return nearby_stadiums
    return db.query(StadiumModel).all()


def get_stadium_by_id(db: Session, std_id):
    return db.query(StadiumModel).filter(StadiumModel.id == std_id).first()


def add_stadium(db: Session, owner, name, description, price, latitude, longitude):
    db_std = StadiumModel(
        owner=owner, name=name, description=description,
        price=price, latitude=latitude, longitude=longitude
    )
    db.add(db_std)
    db.commit()
    db.refresh(db_std)

    return db_std


def update_stadium(db: Session, std_id, data):
    std_query = db.query(StadiumModel).filter(StadiumModel.id == std_id)
    db_std = std_query.first()

    if not db_std:
        raise HTTPException(status_code=404)

    std_query.filter(StadiumModel.id == std_id).update(data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_std)
    return db_std


def delete_std(db, std_id):
    std_query = db.query(StadiumModel).filter(StadiumModel.id == std_id)
    std = std_query.first()
    if not std:
        raise HTTPException(status_code=404,
                            detail=f'No Stadium with this id: {id} found')
    std_query.delete(synchronize_session=False)
    db.commit()
