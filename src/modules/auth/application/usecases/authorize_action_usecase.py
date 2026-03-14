from __future__ import annotations

from uuid import UUID

from src.modules.auth.application.services.permission_evaluator import PermissionEvaluator
from src.modules.auth.application.usecases.resolve_effective_permissions_usecase import (
    ResolveEffectivePermissionsUseCase,
)
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.value_objects.permissions import PermissionCode


class AuthorizeActionUseCase:
    def __init__(
        self,
        *,
        resolve_effective_permissions_usecase: ResolveEffectivePermissionsUseCase,
        permission_evaluator: PermissionEvaluator,
    ) -> None:
        self._resolve_effective_permissions_usecase = resolve_effective_permissions_usecase
        self._permission_evaluator = permission_evaluator

    async def execute(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
        permission_code: str | PermissionCode,
    ) -> bool:
        normalized_permission_code = (
            permission_code if isinstance(permission_code, PermissionCode) else PermissionCode(permission_code)
        )

        resolved_permissions = await self._resolve_effective_permissions_usecase.execute(
            user_id=user_id,
            tenant_id=tenant_id,
        )

        is_allowed = self._permission_evaluator.has_permission(
            resolved_permissions.permissions,
            normalized_permission_code,
        )
        if not is_allowed:
            raise ValidationError("Forbidden action.")

        return True
