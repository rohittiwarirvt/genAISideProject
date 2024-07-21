
from typing import Dict

from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.api.init.deps import get_db
router = APIRouter()


@router.get("")
async def health(db: AsyncSession = Depends(get_db) ) -> Dict[str, str]:
  """Check health of system

  Args:
      db (_type_): db object for checking the connection

  Returns:
      Dict[str, str]: json boject
  """
  await db.execute(text("SELECT 1"))
  return {"status":"alive"}