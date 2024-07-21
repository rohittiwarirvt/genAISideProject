
from fastapi import APIRouter

from app.api import health
from app.api.endpoints import conversation

api_router = APIRouter()

api_router.include_router(
  health.router, prefix="/health", tags=["health"]
)
api_router.include_router(
  conversation.router, prefix="/conversation", tags=["conversation"]
)