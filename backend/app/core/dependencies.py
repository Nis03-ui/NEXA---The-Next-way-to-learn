"""
FastAPI dependency functions for authentication and authorization.
"""
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationException, AuthorizationException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import Role, User
from app.repositories.user_repository import UserRepository

_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Extract and validate JWT; return the active User."""
    if not credentials:
        raise AuthenticationException("Authorization header missing")
    try:
        payload = decode_access_token(credentials.credentials)
        user_id: str = payload["sub"]
    except (JWTError, KeyError):
        raise AuthenticationException("Invalid or expired token")

    repo = UserRepository(db)
    user = await repo.get_by_id(UUID(user_id))
    if user is None:
        raise AuthenticationException("User not found")
    if not user.is_active:
        raise AuthenticationException("Account is deactivated")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: Role):
    """
    Dependency factory that enforces role-based access.

    Usage::

        @router.get("/admin", dependencies=[Depends(require_roles(Role.ADMIN))])
    """

    async def _check(current_user: CurrentUser) -> User:
        if current_user.role not in roles:
            raise AuthorizationException(
                f"This action requires one of the following roles: "
                f"{', '.join(r.value for r in roles)}"
            )
        return current_user

    return _check
