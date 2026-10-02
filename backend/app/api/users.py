from fastapi import APIRouter,Depends
from app.core.security import current_user
from app.models.user import User
from app.schemas.auth import UserOut
router=APIRouter(prefix='/users',tags=['Users'])
@router.get('/me',response_model=UserOut)
async def me(user:User=Depends(current_user)):return user
