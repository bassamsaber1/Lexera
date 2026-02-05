from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from services.auth import bootstrap_admin_password, hash_password
from services.storage import JsonStorage

USERS_PATH = "data/users.json"


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "admin": {
        "contracts.analyze",
        "cases.analyze",
        "memo.create",
        "search.use",
        "chat.open",
        "admin.users.manage",
    },
    "reviewer": {
        "contracts.analyze",
        "cases.analyze",
        "memo.create",
        "search.use",
        "chat.open",
    },
    "viewer": {"search.use", "chat.open"},
}


@dataclass
class UserStore:
    path: str = USERS_PATH

    def __post_init__(self) -> None:
        self.storage = JsonStorage(self.path)
        self.ensure_seed_admin()

    def ensure_seed_admin(self) -> None:
        users = self.list_users()
        if users:
            return

        pwd_hash, salt = hash_password(bootstrap_admin_password())
        admin = {
            "id": str(uuid4()),
            "username": "admin",
            "full_name": "System Admin",
            "password_hash": pwd_hash,
            "password_salt": salt,
            "role": "admin",
            "is_active": True,
            "token_quota": 100000,
            "token_used": 0,
            "violations": [],
            "permissions_override": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.storage.save([admin])

    def list_users(self) -> list[dict[str, Any]]:
        return self.storage.load(default=[])

    def save_users(self, users: list[dict[str, Any]]) -> None:
        self.storage.save(users)

    def find_by_username(self, username: str) -> dict[str, Any] | None:
        for user in self.list_users():
            if user["username"].lower() == username.lower():
                return user
        return None

    def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        for user in self.list_users():
            if user["id"] == user_id:
                return user
        return None

    def can(self, user: dict[str, Any], permission: str) -> bool:
        override = user.get("permissions_override", {}).get(permission)
        if override is not None:
            return bool(override)
        role = user.get("role", "viewer")
        return permission in ROLE_PERMISSIONS.get(role, set())

    def add_user(
        self,
        username: str,
        full_name: str,
        password: str,
        role: str,
        token_quota: int,
    ) -> tuple[bool, str]:
        users = self.list_users()
        if any(u["username"].lower() == username.lower() for u in users):
            return False, "اسم المستخدم موجود بالفعل"
        if role not in ROLE_PERMISSIONS:
            return False, "الدور غير صالح"
        pwd_hash, salt = hash_password(password)
        users.append(
            {
                "id": str(uuid4()),
                "username": username,
                "full_name": full_name,
                "password_hash": pwd_hash,
                "password_salt": salt,
                "role": role,
                "is_active": True,
                "token_quota": token_quota,
                "token_used": 0,
                "violations": [],
                "permissions_override": {},
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        self.save_users(users)
        return True, "تم إضافة المستخدم"

    def update_user(self, user_id: str, updater) -> tuple[bool, str]:
        users = self.list_users()
        found = False
        for idx, user in enumerate(users):
            if user["id"] == user_id:
                users[idx] = updater(user)
                found = True
                break
        if not found:
            return False, "المستخدم غير موجود"

        if not self._has_at_least_one_active_admin(users):
            return False, "لا يمكن تعطيل/حذف آخر Admin"

        self.save_users(users)
        return True, "تم التحديث"

    def delete_user(self, user_id: str) -> tuple[bool, str]:
        users = self.list_users()
        next_users = [u for u in users if u["id"] != user_id]
        if len(next_users) == len(users):
            return False, "المستخدم غير موجود"
        if not self._has_at_least_one_active_admin(next_users):
            return False, "لا يمكن حذف آخر Admin"
        self.save_users(next_users)
        return True, "تم حذف المستخدم"

    @staticmethod
    def _has_at_least_one_active_admin(users: list[dict[str, Any]]) -> bool:
        return any(u.get("role") == "admin" and u.get("is_active") for u in users)
