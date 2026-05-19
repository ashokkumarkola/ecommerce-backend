from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.users.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.modules.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.create_user(
        db,
        payload,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.get_user(
        db,
        user_id,
    )


# @router.get(
#     "/",
#     response_model=list[UserResponse],
# )
# async def get_users(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(20, le=100),
#     db: AsyncSession = Depends(get_db),
# ):
#     return await UserService.get_users(
#         db,
#         skip,
#         limit,
#     )


# @router.put(
#     "/{user_id}",
#     response_model=UserResponse,
# )
# async def update_user(
#     user_id: UUID,
#     payload: UserUpdate,
#     db: AsyncSession = Depends(get_db),
# ):
#     return await UserService.update_user(
#         db,
#         user_id,
#         payload,
#     )


# @router.delete(
#     "/{user_id}",
# )
# async def delete_user(
#     user_id: UUID,
#     db: AsyncSession = Depends(get_db),
# ):
#     return await UserService.delete_user(
#         db,
#         user_id,
#     )