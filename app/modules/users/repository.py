from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


class UserRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        user_data: dict,
    ) -> User:
        user = User(**user_data)

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        user_id: UUID,
    ) -> User | None:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
    ):
        result = await db.execute(
            select(User)
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession,
        user: User,
        update_data: dict,
    ) -> User:
        for key, value in update_data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def delete(
        db: AsyncSession,
        user: User,
    ) -> None:
        await db.delete(user)
        await db.commit()