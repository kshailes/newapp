from fastapi import FastAPI

from app.routers import notes, users

app = FastAPI(title="notes api")
app.include_router(notes.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}
