from typing import List

from fastapi import FastAPI, APIRouter, Depends, Response
from sqlalchemy.orm import Session

from datetime import datetime

from app.core.database import get_db
from app.core.security import authenticate_user
from app.v1.schemas.stadium import StadiumSchema, AddStadiumSchema, UpdateStadiumSchema
from app.v1.services.stadium import add_stadium_srv, get_all_stadiums_srv, get_stadium_srv, update_stadium_srv, \
    delete_std_srv

stadium_router = APIRouter()


@stadium_router.get("/list", response_model=List[StadiumSchema], )
async def std_list_view(
        db: Session = Depends(get_db),
        starts_at: datetime | None = None, ends_at: datetime | None = None,
        radius: float = 5.0, lang: float | None = None, lat: float | None = None,
        user: dict = Depends(authenticate_user)
):
    stds = get_all_stadiums_srv(db, starts_at, ends_at, radius, lang, lat)
    return stds


@stadium_router.get("/{std_id}", response_model=StadiumSchema)
async def get_std_view(std_id: int, db: Session = Depends(get_db), user: dict = Depends(authenticate_user)):
    std = get_stadium_srv(db, std_id)
    return std


@stadium_router.post("/add", response_model=StadiumSchema)
async def add_stadium_view(stadium: AddStadiumSchema, db: Session = Depends(get_db),
                           user: dict = Depends(authenticate_user)):
    std = add_stadium_srv(db, user, stadium)
    return std


@stadium_router.patch("/{std_id}", response_model=StadiumSchema)
async def update_std_view(
        std_id: int, stadium: UpdateStadiumSchema,
        db: Session = Depends(get_db), user: dict = Depends(authenticate_user)
):
    std = update_stadium_srv(db, std_id, user, stadium)
    return std


@stadium_router.delete("/delete/{std_id}")
async def del_std_view(std_id: int, db: Session = Depends(get_db),
                       user: dict = Depends(authenticate_user)):
    delete_std_srv(db, user, std_id)
    return Response(status_code=204)
