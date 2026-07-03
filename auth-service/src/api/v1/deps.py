from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import decode_token
from src.db.postgres import get_db
from src.services.db_user_service import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_token(token)

    except ValueError:
        raise HTTPException(401, "Invalid token")

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(401, "Invalid token")

    repository = UserRepository(db)

    user = await repository.get_by_id(UUID(user_id))

    if user is None:
        raise HTTPException(401, "User not found")

    return user
