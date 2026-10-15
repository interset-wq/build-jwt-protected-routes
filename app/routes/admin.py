"""
管理路由：GET /users（仅 admin）
对标 server/routes/admin.js
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from deps import require_role
from utils.db import read_users

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
def list_users(user: Annotated[dict, Depends(require_role("admin"))]) -> dict:
    users = [
        # 每个user排除passwordHash字段
        {k: v for k, v in u.items() if k != "passwordHash"} for u in read_users()
    ]
    return {"users": users}
