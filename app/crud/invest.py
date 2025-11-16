from datetime import datetime

from sqlalchemy import select

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_funds(session):

    projects = (await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False).order_by(CharityProject.id) # noqa
    )).scalars().all()
    donations = (await session.execute(
        select(Donation).where(
            Donation.fully_invested == False).order_by(Donation.id) # noqa
    )).scalars().all()
    for project in projects:
        if project.fully_invested:
            continue
        for donation in donations:
            if donation.fully_invested:
                continue

            project_invested = (project.invested_amount
                                if project.invested_amount is not None else 0)
            donation_invested = (donation.invested_amount
                                 if donation.invested_amount
                                 is not None else 0)

            need = project.full_amount - project_invested
            remain = donation.full_amount - donation_invested
            to_invest = min(need, remain)

            if to_invest <= 0:
                continue
            project.invested_amount = project_invested + to_invest
            donation.invested_amount = donation_invested + to_invest

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()

            session.add(project)
            session.add(donation)