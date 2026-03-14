from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from src.modules.auth.application.services.auth_cookie_service import AuthCookieService
from src.modules.auth.application.usecases.login_usecase import LoginUseCase
from src.modules.auth.application.usecases.logout_all_usecase import LogoutAllUseCase
from src.modules.auth.application.usecases.logout_usecase import LogoutUseCase
from src.modules.auth.application.usecases.me_usecase import MeUseCase
from src.modules.auth.application.usecases.refresh_session_usecase import RefreshSessionUseCase
from src.modules.auth.application.usecases.register_usecase import RegisterUseCase
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.presentation.http.auth_dependencies import (
    CurrentUserContext,
    get_current_user_context,
    get_login_usecase,
    get_logout_all_usecase,
    get_logout_usecase,
    get_me_usecase,
    get_refresh_session_usecase,
    get_register_usecase,
    require_permissions,
)
from src.modules.auth.presentation.http.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    MeResponse,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    RegisterResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
async def register_endpoint(
    payload: RegisterRequest,
    register_usecase: RegisterUseCase = Depends(get_register_usecase),
) -> RegisterResponse:
    result = await register_usecase.execute(
        email=payload.email,
        password=payload.password,
    )
    return RegisterResponse(user_id=str(result.user.id), email=result.user.email)


@router.post("/login", response_model=LoginResponse)
async def login_endpoint(
    payload: LoginRequest,
    response: Response,
    login_usecase: LoginUseCase = Depends(get_login_usecase),
) -> LoginResponse:
    result = await login_usecase.execute(
        email=payload.email,
        password=payload.password,
        tenant_id=payload.tenant_id,
        user_agent=payload.user_agent,
        ip_address=payload.ip_address,
    )

    cookie_service = AuthCookieService()
    cookie_service.set_access_cookie(response, result.access_token)
    cookie_service.set_refresh_cookie(response, result.refresh_token)

    return LoginResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_endpoint(
    payload: RefreshRequest,
    response: Response,
    refresh_session_usecase: RefreshSessionUseCase = Depends(get_refresh_session_usecase),
) -> RefreshResponse:
    result = await refresh_session_usecase.execute(refresh_token=payload.refresh_token)

    cookie_service = AuthCookieService()
    cookie_service.set_access_cookie(response, result.access_token)
    cookie_service.set_refresh_cookie(response, result.refresh_token)

    return RefreshResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


@router.post("/logout")
async def logout_endpoint(
    payload: LogoutRequest,
    response: Response,
    logout_usecase: LogoutUseCase = Depends(get_logout_usecase),
) -> dict[str, str]:
    await logout_usecase.execute(refresh_token_jti=payload.refresh_token_jti)
    AuthCookieService().clear_auth_cookies(response)
    return {"status": "ok"}


@router.post("/logout-all")
async def logout_all_endpoint(
    current_user: CurrentUserContext = Depends(require_permissions("auth:logout_all")),
    logout_all_usecase: LogoutAllUseCase = Depends(get_logout_all_usecase),
) -> dict[str, int]:
    try:
        revoked_count = await logout_all_usecase.execute(user_id=current_user.user_id)
    except ValidationError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return {"revoked_count": revoked_count}


@router.get(
    "/me",
    response_model=MeResponse,
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"},
    },
)
async def me_endpoint(
    current_user: CurrentUserContext = Depends(require_permissions("auth:me")),
    me_usecase: MeUseCase = Depends(get_me_usecase),
) -> MeResponse:
    try:
        result = await me_usecase.execute(user_id=current_user.user_id)
        return MeResponse(
            id=str(result.user.id),
            email=result.user.email,
            is_active=result.user.is_active,
            is_superuser=result.user.is_superuser,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
