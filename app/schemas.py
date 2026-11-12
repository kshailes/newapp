from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import Note


class NoteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=250)
    description: str = Field(min_length=1)
    user_id: int


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    id: int
    title: str
    description: str
    user_id: int
    is_done: bool
    created_at: datetime
    updated_at: datetime


class NoteUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str | None = Field(default=None, min_length=1, max_length=250)
    description: str | None = Field(default=None, min_length=1)
    is_done: bool | None = None

    @field_validator("title", "description", "is_done")
    @classmethod
    def reject_null(cls, v):
        if v is None:
            raise ValueError("can not be null")
        return v

class UserWithNotes(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    notes: list[NoteRead]

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str
    phone: str | None = None
    password: str = Field(min_length=8, max_length=128)

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    phone: str | None