from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DonationBase(BaseModel):
    full_amount: int = Field(..., ge=0)
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class DonationUpdate(BaseModel):
    full_amount: Optional[int] = Field(None, ge=0)
    comment: Optional[str] = None


class DonationDB(DonationBase):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True