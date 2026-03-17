from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import Depends, Header, HTTPException, Query, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.config import get_settings
from src.core.infrastructure.database.settings.connection import get_session
from src.modules.auth.application.services.auth_metrics_service import AuthMetricsService
from src.modules.auth.application.services.jwt_service import JWTService
from src.modules.auth.application.services.permission_evaluator import PermissionEvaluator
from src.modules.auth.application.services.password_hasher import PasswordHasher
from src.modules.auth.application.services.refresh_token_security import RefreshTokenSecurity
from src.modules.auth.application.usecases.authorize_action_usecase import AuthorizeActionUseCase
from src.modules.auth.application.usecases.login_usecase import LoginUseCase
from src.modules.auth.application.usecases.logout_all_usecase import LogoutAllUseCase
from src.modules.auth.application.usecases.logout_usecase import LogoutUseCase
from src.modules.auth.application.usecases.me_usecase import MeUseCase
from src.modules.auth.application.usecases.resolve_effective_permissions_usecase import (
    ResolveEffectivePermissionsUseCase,
)
from src.modules.auth.application.usecases.refresh_session_usecase import RefreshSessionUseCase
from src.modules.auth.application.usecases.register_usecase import RegisterUseCase
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.value_objects.permissions import PermissionCode
from src.modules.auth.infrastructure.repositories.permission_repository_sqlmodel import PermissionRepositorySQLModel
from src.modules.auth.infrastructure.repositories.refresh_session_repository_sqlmodel import (
    RefreshSessionRepositorySQLModel,
)
from src.modules.auth.infrastructure.repositories.role_permission_repository_sqlmodel import (
    RolePermissionRepositorySQLModel,
)
from src.modules.auth.infrastructure.repositories.user_repository_sqlmodel import UserRepositorySQLModel
from src.modules.auth.infrastructure.repositories.user_tenant_role_repository_sqlmodel import (
    UserTenantRoleRepositorySQLModel,
)

_bearer_scheme = HTTPBearer(auto_error=False)
_auth_metrics_service = AuthMetricsService()


@dataclass(slots=True, frozen=True)
class CurrentUserContext:
    user_id: UUID
    tenant_id: UUID | None
    claims: dict[str, Any]


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_jwt_service() -> JWTService:
    return JWTService()


def get_refresh_token_security() -> RefreshTokenSecurity:
    return RefreshTokenSecurity()


def get_permission_evaluator() -> PermissionEvaluator:
    return PermissionEvaluator()


def get_auth_metrics_service() -> AuthMetricsService:
    return _auth_metrics_service


def get_register_usecase(
    session: AsyncSession = Depends(get_session),
) -> RegisterUseCase:
    user_repository = UserRepositorySQLModel(session)
    password_hasher = get_password_hasher()
    return RegisterUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )


def get_login_usecase(
    session: AsyncSession = Depends(get_session),
) -> LoginUseCase:
    user_repository = UserRepositorySQLModel(session)
    refresh_session_repository = RefreshSessionRepositorySQLModel(session)
    password_hasher = get_password_hasher()
    jwt_service = get_jwt_service()
    refresh_token_security = get_refresh_token_security()
    auth_metrics_service = get_auth_metrics_service()

    return LoginUseCase(
        user_repository=user_repository,
        refresh_session_repository=refresh_session_repository,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
        refresh_token_security=refresh_token_security,
        auth_metrics_service=auth_metrics_service,
    )


def get_refresh_session_usecase(
    session: AsyncSession = Depends(get_session),
) -> RefreshSessionUseCase:
    refresh_session_repository = RefreshSessionRepositorySQLModel(session)
    jwt_service = get_jwt_service()
    refresh_token_security = get_refresh_token_security()
    auth_metrics_service = get_auth_metrics_service()

    return RefreshSessionUseCase(
        refresh_session_repository=refresh_session_repository,
        jwt_service=jwt_service,
        refresh_token_security=refresh_token_security,
        auth_metrics_service=auth_metrics_service,
    )


def get_logout_usecase(
    session: AsyncSession = Depends(get_session),
) -> LogoutUseCase:
    refresh_session_repository = RefreshSessionRepositorySQLModel(session)
    auth_metrics_service = get_auth_metrics_service()
    return LogoutUseCase(
        refresh_session_repository=refresh_session_repository,
        auth_metrics_service=auth_metrics_service,
    )


def get_logout_all_usecase(
    session: AsyncSession = Depends(get_session),
) -> LogoutAllUseCase:
    refresh_session_repository = RefreshSessionRepositorySQLModel(session)
    auth_metrics_service = get_auth_metrics_service()
    return LogoutAllUseCase(
        refresh_session_repository=refresh_session_repository,
        auth_metrics_service=auth_metrics_service,
    )


def get_me_usecase(
    session: AsyncSession = Depends(get_session),
) -> MeUseCase:
    user_repository = UserRepositorySQLModel(session)
    return MeUseCase(user_repository=user_repository)


def get_resolve_effective_permissions_usecase(
    session: AsyncSession = Depends(get_session),
) -> ResolveEffectivePermissionsUseCase:
    user_repository = UserRepositorySQLModel(session)
    user_tenant_role_repository = UserTenantRoleRepositorySQLModel(session)
    role_permission_repository = RolePermissionRepositorySQLModel(session)
    permission_repository = PermissionRepositorySQLModel(session)

    return ResolveEffectivePermissionsUseCase(
        user_repository=user_repository,
        user_tenant_role_repository=user_tenant_role_repository,
        role_permission_repository=role_permission_repository,
        permission_repository=permission_repository,
    )


def get_authorize_action_usecase(
    session: AsyncSession = Depends(get_session),
) -> AuthorizeActionUseCase:
    resolve_effective_permissions_usecase = get_resolve_effective_permissions_usecase(session)
    permission_evaluator = get_permission_evaluator()

    return AuthorizeActionUseCase(
        resolve_effective_permissions_usecase=resolve_effective_permissions_usecase,
        permission_evaluator=permission_evaluator,
    )


def get_tenant_context(
    request: Request,
    tenant_id_query: str | None = Query(default=None, alias="tenant_id"),
    x_tenant_id: str | None = Header(default=None, alias="X-Tenant-Id"),
    tenant_id_path: str | None = None,
) -> UUID | None:
    # Preferência de resolução de tenant: path -> query -> header.
    # Mantém compatibilidade com diferentes estilos de roteamento (path/query/header).
    candidate_tenant = tenant_id_path or tenant_id_query or x_tenant_id or request.headers.get("x-tenant-id")
    if candidate_tenant is None:
        return None

    tenant_value = candidate_tenant.strip()
    if not tenant_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant context is invalid.",
        )

    try:
        return UUID(tenant_value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant context is invalid.",
        ) from exc


def get_current_user_context(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    jwt_service: JWTService = Depends(get_jwt_service),
    tenant_id: UUID | None = Depends(get_tenant_context),
) -> CurrentUserContext:
    settings = get_settings()
    bearer_token = credentials.credentials if credentials else None
    cookie_token = request.cookies.get(settings.ACCESS_COOKIE_NAME)
    raw_token = bearer_token or cookie_token

    if not raw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    try:
        claims = jwt_service.decode_token(raw_token, expected_type="access")
        user_id = UUID(str(claims.get("sub", "")).strip())
    except (ValidationError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        ) from exc

    token_tenant_raw = claims.get("tenant_id")
    if tenant_id is not None:
        resolved_tenant = tenant_id
    elif token_tenant_raw is not None:
        try:
            resolved_tenant = UUID(str(token_tenant_raw).strip())
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid tenant claim in token.",
            ) from exc
    else:
        resolved_tenant = None

    return CurrentUserContext(
        user_id=user_id,
        tenant_id=resolved_tenant,
        claims=claims,
    )


def require_permissions(*permission_codes: str):
    async def _dependency(
        current_user: CurrentUserContext = Depends(get_current_user_context),
        authorize_action_usecase: AuthorizeActionUseCase = Depends(get_authorize_action_usecase),
    ) -> CurrentUserContext:
        if current_user.tenant_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tenant context is required for authorization.",
            )

        for permission_code in permission_codes:
            try:
                await authorize_action_usecase.execute(
                    user_id=current_user.user_id,
                    tenant_id=current_user.tenant_id,
                    permission_code=PermissionCode(permission_code),
                )
            except ValidationError as exc:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=str(exc),
                ) from exc

        return current_user

    return _dependency
