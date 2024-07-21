
from fastapi import FastAPI
import uvicorn

from app.core.config import settings
from app.api.routes import api_router

app = FastAPI(
  title=settings.PROJECT_NAME,
  openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_PREFIX)
# app.mount(f"/{settings.LOADER_IO_VERIFICATION_STR}", loader_io_router)

def start():
  print("Running in AppEnvironment: " + settings.ENVIRONMENT)
  live_reload: bool = settings.SHOULD_ENVIRONMENT_RELOAD
  uvicorn.run(
    "app.restserver:app",
    host="0.0.0.0",
    port=8000,
    reload=live_reload,
    workers=settings.UVICORN_WORKER_COUNT
  )

# for debugging via vscode
if __name__== "__main__":
    start()