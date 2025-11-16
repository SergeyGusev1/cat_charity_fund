from datetime import datetime
from sqlalchemy import select
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_funds(session):
    # все открытые проекты
    projects = (await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == False).order_by(CharityProject.id)
    )).scalars().all()
    donations = (await session.execute(
        select(Donation).where(Donation.fully_invested == False).order_by(Donation.id)
    )).scalars().all()
    for project in projects:
        if project.fully_invested:
            continue
        for donation in donations:
            if donation.fully_invested:
                continue
            need = project.full_amount - (project.invested_amount or 0)
            remain = donation.full_amount - (donation.invested_amount or 0)
            to_invest = min(need, remain)
            if to_invest <= 0:
                continue
            project.invested_amount = (project.invested_amount or 0) + to_invest
            donation.invested_amount = (donation.invested_amount or 0) + to_invest
            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.utcnow()
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.utcnow()
            session.add(project)
            session.add(donation)