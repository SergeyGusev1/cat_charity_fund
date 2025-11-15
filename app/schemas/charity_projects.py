from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field


class CharityProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: int = Field(ge=0)


class CharityProjectsCreate(CharityProjectBase):
    pass


class CharityProjectsUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(ge=0)


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True