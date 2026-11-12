from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.database import get_db
from app.models import User
from app.schemas import UserWithNotes, UserRead, UserCreate
from app.security import hash_password

DbSession = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["users"])


def get_user_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}", response_model=UserWithNotes)
def get_users(user_id: int, db: DbSession):
    return get_user_or_404(db, user_id=user_id)

@router.get("", response_model=List[UserWithNotes])
def list_users(db: DbSession, skip: int = Query(0,ge = 0), limit: int = Query(10, ge=1, le = 100)):
    stmt = select(User).order_by(User.id).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.post("/register", response_model=UserRead, status_code=201)
def create_user(db: DbSession, payload: UserCreate) -> User:
    user = db.scalars(select(User).where(User.email == payload.email)).first()
    if user is not None:
        raise HTTPException(status_code=409, detail="User already exists")
    user = User(**payload.model_dump(exclude={"password"}))
    user.hashed_password = hash_password(payload.password)
    user.email = payload.email.lower()
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    db.refresh(user)
    return user