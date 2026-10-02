from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_roles
from app.db.session import get_db
from app.models.content import Content
from app.models.user import Role, User
from app.schemas.content import ContentCreate, ContentOut, ContentUpdate
from app.services.indexing import ContentIndexingService


router = APIRouter(prefix="/teacher", tags=["Teacher"])


@router.post(
    "/content",
    response_model=ContentOut,
)
async def create_content(
    data: ContentCreate,
    user: User = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    content = Content(
        title=data.title,
        description=data.description,
        body=data.body,
        subject=data.subject,
        published=data.published,
        author_id=user.id,
    )

    db.add(content)

    await db.flush()

    indexing_service = ContentIndexingService()

    await indexing_service.index_content(
        content=content,
        db=db,
    )

    await db.commit()
    await db.refresh(content)

    return content


@router.get(
    "/content",
    response_model=list[ContentOut],
)
async def get_content(
    user: User = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Content)
        .order_by(Content.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/content/{content_id}",
    response_model=ContentOut,
)
async def get_content_by_id(
    content_id: int,
    user: User = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    content = await db.get(Content, content_id)

    if not content:
        raise HTTPException(
            status_code=404,
            detail="Content not found",
        )

    return content


@router.patch(
    "/content/{content_id}",
    response_model=ContentOut,
)
async def update_content(
    content_id: int,
    data: ContentUpdate,
    user: User = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    content = await db.get(Content, content_id)

    if not content:
        raise HTTPException(
            status_code=404,
            detail="Content not found",
        )

    if user.role != Role.ADMIN and content.author_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only modify your own content",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(content, field, value)

    await db.flush()

    indexing_service = ContentIndexingService()

    await indexing_service.index_content(
        content=content,
        db=db,
    )

    await db.commit()
    await db.refresh(content)

    return content


@router.delete("/content/{content_id}")
async def delete_content(
    content_id: int,
    user: User = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    content = await db.get(Content, content_id)

    if not content:
        raise HTTPException(
            status_code=404,
            detail="Content not found",
        )

    if user.role != Role.ADMIN and content.author_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own content",
        )

    await db.delete(content)
    await db.commit()

    return {"message": "Content deleted successfully"}