from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_valid, check_name_duplicate,
                                check_project_exists,
                                check_project_no_invested_funds,
                                check_project_not_closed)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

project_router = APIRouter()


@project_router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charityproject_crud.create_with_invest(
        project, session)
    return new_project


@project_router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Для все пользователей."""
    all_projects = await charityproject_crud.get_multi(session)
    return all_projects


@project_router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charityproject(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    check_project_not_closed(project)
    if obj_in.full_amount is not None:
        check_full_amount_valid(obj_in.full_amount, project.invested_amount)

    updated_project = await charityproject_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session
    )

    return updated_project


@project_router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    check_project_no_invested_funds(project)
    deleted_project = await charityproject_crud.remove(project, session)
    return deleted_project