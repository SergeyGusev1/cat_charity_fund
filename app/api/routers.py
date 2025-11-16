from fastapi import APIRouter

from app.api.endpoints import project_router, users_router

main_router = APIRouter()
main_router.include_router(
    project_router, prefix='/charity_project', tags=['Charity Projects'])
main_router.include_router(users_router, tags=['Users'])