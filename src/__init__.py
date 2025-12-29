from fastapi import FastAPI, APIRouter

from src.api import wallet
from src.core.config import settings
app = FastAPI()

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(wallet.router)
app.include_router(api_router)