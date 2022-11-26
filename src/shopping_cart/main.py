from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from shopping_cart import settings
from shopping_cart.api.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url='{}/openapi.json'.format(settings.API_STR)
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_STR)
