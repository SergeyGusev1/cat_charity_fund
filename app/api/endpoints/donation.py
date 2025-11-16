from fastapi import APIRouter, Depends
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationDB, DonationDBSuper
from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.crud.donation import donation_crud


donation_router = APIRouter()


@donation_router.post('/', response_model=DonationDB)
async def create_donate(
    donation_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create_with_invest(
        donation_in,
        user,
        session
    )
    return new_donation


@donation_router.get('/my', response_model=list[DonationDB])
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    all_donations_user = await donation_crud.get_donation_user(user.id, session)
    return all_donations_user


@donation_router.get(
    '/',
    response_model=list[DonationDBSuper],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations