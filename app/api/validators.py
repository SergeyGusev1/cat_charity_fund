from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models.charity_project import CharityProject


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    project = await session.get(CharityProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project_id = await charityproject_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Not unique name'
        )


def check_project_not_closed(project):
    if project.fully_invested:
        raise HTTPException(status_code=400,
                            detail="Нельзя менять закрытый проект")


def check_full_amount_valid(new_amount, invested_amount):
    if new_amount is not None and new_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail="Новая сумма должна быть не меньше внесённой"
        )


def check_project_no_invested_funds(project):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить проект, в который уже внесли средства"
        )
