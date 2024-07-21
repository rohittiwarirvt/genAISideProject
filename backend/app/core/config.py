
import os
from pydantic_settings import BaseSettings
from pydantic import EmailStr, validator


class Settings(BaseSettings):
  DATABASE_URL: str
  S3_BUCKET_NAME: str
  API_PREFIX: str = "/api"

  PROJECT_NAME: str
  S3_ASSET_BUCKET_NAME: str

  VECTOR_STORE_INDEX_NAME: str = "opensearch_vector_store"
  OPEN_API_KEY: str
  LOADER_IO_VERIFICATION_STR: str = "loaderio-e51043c635e0f4656473d3570ae5d9ec"
  ENVIRONMENT: str
  SHOULD_ENVIRONMENT_RELOAD: bool

  @validator("DATABASE_URL", pre=True)
  def assemble_db_url(cls, value: str):
    if not value and not value.startswith("postgres"):
      raise ValueError("Ivalid Database url value not present" + str(value))
    return (
      value.replace("postgres://", "postgresql://")
      .replace("postgresql://", "postgresql+asyncpg://")
      .strip()
    )

  @property
  def UVICORN_WORKER_COUNT(self) -> int:
    if self.ENVIRONMENT == "dev":
      return 1

    return 3



settings = Settings()
os.environ["OPEN_API_KEY"] = settings.OPEN_API_KEY