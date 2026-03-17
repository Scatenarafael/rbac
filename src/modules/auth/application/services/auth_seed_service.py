from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid5

from src.modules.auth.domain.entities.permission import Permission
from src.modules.auth.domain.entities.role import Role
from src.modules.auth.domain.entities.role_permission import RolePermission
from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.repository_interfaces.permission_repository import IPermissionRepository
from src.modules.auth.domain.repository_interfaces.role_permission_repository import IRolePermissionRepository
from src.modules.auth.domain.repository_interfaces.role_repository import IRoleRepository
from src.modules.auth.domain.repository_interfaces.user_repository import IUserRepository
from src.modules.auth.domain.value_objects.emails import Email

SEED_NAMESPACE = UUID("11111111-2222-3333-4444-555555555555")

DEFAULT_PERMISSIONS: tuple[tuple[str, str], ...] = (
    ("auth:me", "Read authenticated user profile"),
    ("auth:logout_all", "Revoke all refresh sessions from current user"),
    ("users:read", "Read users in tenant scope"),
)

DEFAULT_ROLE_PERMISSIONS: dict[str, tuple[str, ...]] = {
    "admin": ("auth:me", "auth:logout_all", "users:read"),
    "member": ("auth:me",),
}


@dataclass(slots=True)
class AuthSeedService:
    permission_repository: IPermissionRepository
    role_repository: IRoleRepository
    role_permission_repository: IRolePermissionRepository
    user_repository: IUserRepository

    async def seed_defaults(
        self,
        *,
        admin_email: str | None = None,
        admin_password_hash: str | None = None,
    ) -> dict[str, int]:
        """
        Seed idempotent de permissões/roles/admin padrão.
        Execuções repetidas devem ser seguras e sem duplicidade.
        """
        created_permissions = await self._seed_permissions()
        created_roles = await self._seed_roles()
        created_role_permissions = await self._seed_role_permissions()
        created_admin_user = await self._seed_admin_user(
            admin_email=admin_email,
            admin_password_hash=admin_password_hash,
        )

        return {
            "permissions_created": created_permissions,
            "roles_created": created_roles,
            "role_permissions_created": created_role_permissions,
            "admin_users_created": created_admin_user,
        }

    async def _seed_permissions(self) -> int:
        created = 0
        for permission_name, description in DEFAULT_PERMISSIONS:
            permission_id = self._stable_id("permission", permission_name)
            existing = await self.permission_repository.get_by_id(permission_id)
            if existing is not None:
                continue

            await self.permission_repository.create(
                Permission(id=permission_id, name=permission_name, description=description)
            )
            created += 1
        return created

    async def _seed_roles(self) -> int:
        created = 0
        for role_name in DEFAULT_ROLE_PERMISSIONS:
            role_id = self._stable_id("role", role_name)
            existing = await self.role_repository.get_by_id(role_id)
            if existing is not None:
                continue

            await self.role_repository.create(
                Role(id=role_id, name=role_name, description=f"Default role: {role_name}")
            )
            created += 1
        return created

    async def _seed_role_permissions(self) -> int:
        created = 0
        for role_name, permission_names in DEFAULT_ROLE_PERMISSIONS.items():
            role_id = self._stable_id("role", role_name)
            existing_role_permissions = await self.role_permission_repository.list_by_role_ids([role_id])
            existing_pairs = {(item.role_id, item.permission_id) for item in existing_role_permissions}

            for permission_name in permission_names:
                permission_id = self._stable_id("permission", permission_name)
                pair = (role_id, permission_id)
                if pair in existing_pairs:
                    continue

                await self.role_permission_repository.create(
                    RolePermission(role_id=role_id, permission_id=permission_id)
                )
                existing_pairs.add(pair)
                created += 1
        return created

    async def _seed_admin_user(self, *, admin_email: str | None, admin_password_hash: str | None) -> int:
        if not admin_email or not admin_password_hash:
            return 0

        normalized_email = Email(admin_email)
        existing_user = await self.user_repository.get_by_email(normalized_email)
        if existing_user is not None:
            if not existing_user.is_superuser:
                existing_user.grant_superuser()
                await self.user_repository.update(existing_user.id, existing_user)
            return 0

        user_id = self._stable_id("user", normalized_email.value)
        user = User(
            id=user_id,
            email=normalized_email.value,
            password_hash=admin_password_hash,
            is_superuser=True,
        )
        await self.user_repository.create(user)
        return 1

    @staticmethod
    def _stable_id(prefix: str, value: str) -> UUID:
        return uuid5(SEED_NAMESPACE, f"{prefix}:{value.strip().lower()}")
