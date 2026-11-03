from fastapi import  Depends, HTTPException, Query, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Note, User
from app.schemas import NoteRead, NoteCreate, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

def get_note_or_404(db: Session, note_id: int) -> Note:
    note = db.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    return get_note_or_404(db=db, note_id=note_id)


@router.get("", response_model=list[NoteRead])
def list_notes(skip: int = Query(0,ge = 0), limit: int = Query(10,ge=1,le= 100), db: Session = Depends(get_db)):
    stmt = select(Note).order_by(Note.id).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.post("", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    note = Note(**payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.patch("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload:NoteUpdate, db: Session = Depends(get_db)):
    note = get_note_or_404(db=db, note_id=note_id)
    for key,value in payload.model_dump(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note_or_404(db=db, note_id=note_id)
    db.delete(note)
    db.commit()