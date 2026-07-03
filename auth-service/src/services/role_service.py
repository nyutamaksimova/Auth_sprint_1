from uuid import UUID

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserRole
from src.services.db_user_service import UserRepository


class RoleService:

    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def assign_role(self, user_id: UUID, role: UserRole):

        user = await self.repository.update_role(user_id, role)

        if user is None:
            raise HTTPException(404, "User not found")

        return user

    async def revoke_role(self, user_id: UUID):

        user = await self.repository.update_role(user_id, UserRole.USER)

        if user is None:
            raise HTTPException(404, "User not found")

        return user
