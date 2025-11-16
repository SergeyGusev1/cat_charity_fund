from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationUpdate
from app.services.services import invest_funds


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    DonationUpdate
]):

    async def create_with_invest(self, donation_in, user, session):
        new_donation = Donation(
            full_amount=donation_in.full_amount,
            user_id=user.id,
            invested_amount=0,
            fully_invested=False,
            create_date=datetime.now(),
            comment=getattr(donation_in, "comment", None),
        )
        session.add(new_donation)
        await session.flush()
        await invest_funds(session)
        await session.commit()
        await session.refresh(new_donation)
        return new_donation

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(Donation.id).where(
                Donation.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_donation_user(
        self,
        user_id: int,
        session: AsyncSession
    ) -> Optional[list[Donation]]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )

        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)