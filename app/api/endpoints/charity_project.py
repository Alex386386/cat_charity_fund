from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_exists,
    check_the_opportunity_to_delete,
    check_the_opportunity_to_update_project,
    check_the_unique_project_name,
    check_the_unique_project_name_update
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDeleteDB,
    CharityProjectUpdateDB,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_the_unique_project_name(charity_project.name, session)
    new_project = await charity_project_crud.create_project(
        charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectUpdateDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_exists(project_id, session)
    project = await check_the_opportunity_to_update_project(project, obj_in)
    await check_the_unique_project_name_update(
        obj_in.name, project_id, session)
    updated_project = await charity_project_crud.update_project(
        project, obj_in, session
    )
    return updated_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDeleteDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    project_obj = await check_exists(
        project_id, session
    )
    await check_the_opportunity_to_delete(project_obj)
    meeting_room = await charity_project_crud.remove(project_obj, session)
    return meeting_room
