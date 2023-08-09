from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import Donation, User, CharityProject


class CRUDDonation(CRUDBase):

    async def create_donation(
            self,
            obj_in,
            user: User,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['create_date'] = datetime.now()
        obj_in_data['user_id'] = user.id
        obj_in_data['invested_amount'] = 0
        db_donation = self.model(**obj_in_data)

        projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested == False)
            .order_by(CharityProject.create_date)
        )
        projects = projects.scalars().all()
        if projects:
            for project in projects:
                project_invested = project.invested_amount
                need_to_full = project.full_amount - project.invested_amount
                donation_able_to_invest = (
                        db_donation.full_amount - db_donation.invested_amount)

                if need_to_full >= donation_able_to_invest:
                    project.invested_amount = (
                            project_invested + donation_able_to_invest)
                    if project.invested_amount == project.full_amount:
                        project.fully_invested = True
                        project.close_date = datetime.now()
                    db_donation.invested_amount = db_donation.full_amount
                    db_donation.fully_invested = True
                    db_donation.close_date = datetime.now()
                    break
                elif need_to_full < donation_able_to_invest:
                    db_donation.invested_amount += need_to_full
                    project.invested_amount = project.full_amount
                    project.fully_invested = True
                    project.close_date = datetime.now()

        session.add(db_donation)
        await session.commit()
        await session.refresh(db_donation)
        return db_donation

    async def get_my(
            self,
            user: User,
            session: AsyncSession,
    ) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        if not donations:
            return []
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
