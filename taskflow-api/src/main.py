from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_db, init_db, close_db
from src.routes import api_router

app = FastAPI(
    title="TaskFlow API",
    description="Async Task Management API",
    version="1.0.0"
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager."""
    await init_db()
    yield
    await close_db()


@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(api_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to TaskFlow API"}
