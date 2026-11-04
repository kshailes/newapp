from fastapi import FastAPI

from app.routers import notes

app = FastAPI(title="notes api")
app.include_router(notes.router)


@app.get("/health")
def health():
    return {"status": "ok"}
