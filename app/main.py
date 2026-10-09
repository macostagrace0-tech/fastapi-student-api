import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import items


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Student Item API",
    version="1.0.0",
    lifespan=lifespan,
)


origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items.router)


@app.get("/")
def root():
    return {"message": "Student Item API is running"}


@app.get("/health")
def health():
    logger.info("Health endpoint called")
    return {"status": "healthy"}
