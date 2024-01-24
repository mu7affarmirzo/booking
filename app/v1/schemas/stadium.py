from pydantic import BaseModel


class StadiumSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int
    latitude: float
    longitude: float
    owner_id: int


class AddStadiumSchema(BaseModel):
    name: str
    description: str
    price: int
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class UpdateStadiumSchema(BaseModel):
    name: str = None
    description: str = None
    price: int = None
    latitude: float = None
    longitude: float = None

    owner_id: int = None

    class Config:
        orm_mode = True
