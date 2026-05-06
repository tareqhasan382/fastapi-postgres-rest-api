from fastapi import FastAPI
from app.database import Base, engine
from app.routers import items

Base.metadata.create_all(bind=engine)  # table auto-create (dev only)

app = FastAPI(title="EventCart API", version="1.0.0")

app.include_router(items.router)

@app.get("/health")
def health():
    return {"status": "ok"}