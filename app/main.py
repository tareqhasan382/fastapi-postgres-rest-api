from fastapi import FastAPI
# from app.database import Base, engine
from app.routers import items,auth

#Base.metadata.create_all(bind=engine)  # table auto-create (dev only)

app = FastAPI(title="FastAPI CRUD API", version="2.0.0")

app.include_router(auth.router)
app.include_router(items.router)

@app.get("/health")
def health():
    return {"status": "ok"}