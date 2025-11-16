from typing import Optional
from datetime import datetime
from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import (DonationCreate,
                                  DonationUpdate)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    DonationUpdate
]):

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
        project_id = project_id.scalars().first()
        return project_id

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
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)