from collections.abc import Generator

from fastapi import Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, selectinload

# import app.models
# from ./app.config import get_settings
from app.models import User

DATABASE_URL="postgresql+psycopg://notes:notes@localhost:5433/notes"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(bind=engine)

def add_users():
    with SessionLocal() as db:
        user1 = User(name="Shailesh1", email="Shailesh1@gmail.com")
        user2 = User(name="Shailesh2", email="Shailesh2@gmail.com")
        user3 = User(name="Shailesh3", email="Shailesh3@gmail.com")
        db.add_all([user1,user2,user3])
        db.commit()

def fetch_all_users():
    stmt = select(User).options(selectinload(User.notes)).order_by(User.id)
    with SessionLocal() as db:
        users = db.scalars(stmt).all()
        for user in users:
            print(user.id, user.name, user.notes)


if __name__ == "__main__":
    # add_users()
    fetch_all_users()
