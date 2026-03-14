from __future__ import annotations

from collections.abc import Iterable

from src.modules.auth.domain.value_objects.permissions import PermissionCode


class PermissionEvaluator:
    def has_permission(self, effective_permissions: Iterable[str], permission_code: PermissionCode) -> bool:
        normalized_permissions = {permission.strip().lower() for permission in effective_permissions}
        target_permission = permission_code.value.strip().lower()

        if "*" in normalized_permissions:
            return True

        return target_permission in normalized_permissions
