from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCharityRepository
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(
    BaseCharityRepository[
        CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
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


charityproject_crud = CRUDCharityProject(CharityProject)
