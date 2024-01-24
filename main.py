from fastapi import FastAPI

from app.main import router as api_router
from app.core.config import Settings

app = FastAPI()
settings = Settings()


if settings.is_testing:
    print('TESTING THE BUG', settings.is_testing)

if not settings.is_production:
    from fastapi.middleware.cors import CORSMiddleware

    # Allow CORS for development and testing
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Set this to your frontend's URL in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api/v1")

