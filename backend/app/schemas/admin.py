
from pydantic import BaseModel

from app.models.user import Role


class RoleUpdate(BaseModel):
    role: Role


class AdminUserOut(BaseModel):
    id: int
    name: str
    email: str
    role: Role

    model_config = {"from_attributes": True}
