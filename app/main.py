from fastapi import FastAPI
from app.routers import items, auth
import subprocess

app = FastAPI(title="FastAPI CRUD API", version="2.0.0")

@app.on_event("startup")
def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"], check=True)

app.include_router(auth.router)
app.include_router(items.router)

@app.get("/health")
def health():
    return {"status": "ok"}