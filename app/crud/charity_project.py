from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )

        return project_id.scalars().first()

    async def update(
            self,
            db_obj: CharityProject,
            obj_in: CharityProjectUpdate,
            session: AsyncSession
    ):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj


charityproject_crud = CRUDCharityProject(CharityProject)
