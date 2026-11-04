from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.models import User
from app.schemas import UserWithNotes

DbSession = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["users"])


def get_user_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return user


@router.get("/{user_id}", response_model=UserWithNotes)
def get_users(user_id: int, db: DbSession):
    return get_user_or_404(db, user_id=user_id)
