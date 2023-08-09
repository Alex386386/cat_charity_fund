from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100,
        title='Название проекта',
        example='Соберём на корм кошкам!',
    )
    description: str = Field(
        ..., min_length=1,
        title='Описание проекта',
        example='Кошечки голодают, нам нужно им помочь!',
    )
    full_amount: PositiveInt = Field(..., example=1350)

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100,
        title='Название проекта',
        example='Соберём на корм кошкам!',
    )
    description: Optional[str] = Field(
        None, min_length=1,
        title='Описание проекта',
        example='Кошечки голодают, нам нужно им помочь!',
    )
    full_amount: Optional[PositiveInt] = Field(None, example=1350)


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectDeleteDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdateDB(CharityProjectDB):
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
