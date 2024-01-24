from fastapi import APIRouter
from app.v1.routers import bookings, stadiums, auth
from fastapi import FastAPI


router = APIRouter()
app = FastAPI()

router.include_router(bookings.booking_router, prefix="/bookings", tags=['bookings'])
router.include_router(stadiums.stadium_router, prefix="/stadiums", tags=['stadiums'])
router.include_router(auth.auth_routers, prefix="/auth", tags=['auth'])


