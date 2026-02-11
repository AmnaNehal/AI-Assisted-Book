from fastapi import FastAPI
from api.health import router as health_router
from api.query import router as query_router
from config.settings import settings
from utils.logging import setup_logging
from utils.error_handling import setup_error_handlers
from fastapi.middleware.cors import CORSMiddleware

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# 🔥 CORS (MANDATORY FOR FRONTEND)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_error_handlers(app)

app.include_router(health_router, prefix="/api")
app.include_router(query_router, prefix="/api")

# backend_rag/main.py
@app.get("/")
async def root():
    return {"message": "Backend is running!"}
