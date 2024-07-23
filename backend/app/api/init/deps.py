
from typing import Generator
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
# from open
from llama_index.vector_stores.opensearch import OpensearchVectorClient
from contextlib import asynccontextmanager

from app.db.session import SessionLocal
from app.core.config import settings

async def get_db() -> Generator[AsyncSession, None, None]:
  async with SessionLocal() as db:
    try:
      yield db
      await db.commit()
    except Exception:
      await db.rollback()
      raise
    finally:
      await db.close()

# @asynccontextmanager
# async def lifespan(app: FastAPI):

#   client = OpensearchVectorClient(settings.OPENSEARCH_ENDPOINT, settings.OPENSEARCH_INDEX, 1536)
#   app.state.opensearch_client = client
#   yield