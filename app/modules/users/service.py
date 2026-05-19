from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    UserCreate,
    UserUpdate,
)
from app.core.security import hash_password

class UserService:

    @staticmethod
    async def create_user(
        db: AsyncSession,
        payload: UserCreate,
    ):
        existing_user = await UserRepository.get_by_email(
            db,
            payload.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user_data = payload.model_dump()

        password = user_data.pop("password")

        user_data["password_hash"] = hash_password(password)

        return await UserRepository.create(
            db,
            user_data,
        )

    @staticmethod
    async def get_user(
        db: AsyncSession,
        user_id: UUID,
    ):
        user = await UserRepository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    @staticmethod
    async def get_users(
        db: AsyncSession,
        skip: int,
        limit: int,
    ):
        return await UserRepository.get_all(
            db,
            skip,
            limit,
        )

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: UUID,
        payload: UserUpdate,
    ):
        user = await UserRepository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        return await UserRepository.update(
            db,
            user,
            update_data,
        )

    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user_id: UUID,
    ):
        user = await UserRepository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await UserRepository.delete(db, user)

        return {"message": "User deleted successfully"}