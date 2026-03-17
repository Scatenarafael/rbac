from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import MetaData

from src.core.config.config import get_settings
from src.modules.auth.application.services.auth_production_validator import AuthProductionValidator
from src.modules.auth.presentation.http.routers.auth_router import router as auth_router

# from src.core.errors.base import BaseAppException
# from src.core.http.exception_handlers import (
#     app_exception_handler,
#     http_exception_handler,
#     sqlalchemy_error_handler,
#     sqlalchemy_integrity_handler,
#     timeout_handler,
#     unhandled_exception_handler,
#     validation_exception_handler,
# )
# from src.infrastructure.logging.config import configure_logging
# from src.modules.core.presentation.http.middlewares.auth_middleware import AuthMiddleware
# from src.modules.core.presentation.http.middlewares.request_id import RequestIdMiddleware
# from src.modules.core.presentation.http.middlewares.request_logging import RequestLoggingMiddleware
# from src.modules.core.presentation.http.routers.auth import auth_router
# from src.modules.core.presentation.http.routers.email import email_router
# from src.modules.core.presentation.http.routers.users import user_router

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://192.168.15.7:5173",
    "http://192.168.15.6:5173",
    "http://192.168.1.120:4173",
    "http://192.168.1.120:5173",
]

metadata = MetaData()


def create_app() -> FastAPI:
    # configure_logging(level="INFO")

    app = FastAPI()
    settings = get_settings()

    # Production checklist validation should run on startup before serving requests.
    if "localhost" not in settings.SERVER_URL:
        validator = AuthProductionValidator(settings=settings)
        validator.validate()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)

    return app
