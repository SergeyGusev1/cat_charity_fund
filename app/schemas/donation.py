from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class DonationUpdate(BaseModel):
    full_amount: Optional[PositiveInt] = None
    comment: Optional[str] = None


class DonationDB(DonationBase):
    id: int
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDBSuper(DonationDB):
    user_id: Optional[int] = None
    invested_amount: Optional[int] = None
    fully_invested: Optional[bool] = None