from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


class CRUDCharityProject(CRUDBase):

    async def create_project(
            self,
            obj_in,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['create_date'] = datetime.now()
        obj_in_data['invested_amount'] = 0
        obj_in_data['close_date'] = None
        d_project = self.model(**obj_in_data)
        if d_project.full_amount != 0:
            donations = await session.execute(
                select(Donation)
                .where(Donation.fully_invested == False)
                .order_by(Donation.create_date)
            )
            donations = donations.scalars().all()
            if donations:
                for donation in donations:
                    project_invested = d_project.invested_amount
                    need_to_full = (
                            d_project.full_amount - d_project.invested_amount)
                    donation_able_to_invest = (
                            donation.full_amount - donation.invested_amount)

                    if need_to_full >= donation_able_to_invest:
                        d_project.invested_amount = (
                                project_invested + donation_able_to_invest)
                        if d_project.invested_amount == d_project.full_amount:
                            d_project.fully_invested = True
                            d_project.close_date = datetime.now()
                        donation.invested_amount = donation.full_amount
                        donation.fully_invested = True
                        donation.close_date = datetime.now()
                        continue
                    elif need_to_full < donation_able_to_invest:
                        donation.invested_amount += need_to_full
                        d_project.invested_amount = d_project.full_amount
                        d_project.fully_invested = True
                        d_project.close_date = datetime.now()
                        break
        elif d_project.full_amount == 0:
            d_project.fully_invested = True
            d_project.close_date = d_project.create_date

        session.add(d_project)
        await session.commit()
        await session.refresh(d_project)
        return d_project

    async def update_project(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.invested_amount == db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
