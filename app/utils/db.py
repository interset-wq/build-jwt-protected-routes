"""
模拟数据库CRUD
"""

import json
from pathlib import Path
from uuid import UUID

DB_PATH = Path(__file__).parent.parent / "data/users.json"


def read_users() -> list[dict]:
    with open(DB_PATH, encoding="utf-8") as f:
        users = json.load(f)
    return users


def write_users(updated: list[dict]) -> None:
    """使用updated列表覆盖json文件的内容"""
    with open(DB_PATH, encoding="utf-8") as f:
        content = f.read()
    new_content = json.dumps(updated, indent=2, ensure_ascii=False)
    if content == new_content:
        return
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)


def read_by_email(email: str) -> dict | None:
    users: list[dict] = read_users()
    for user in users:
        if user["email"] == email:
            return user
    return None


def read_by_id(id: UUID) -> dict | None:
    users: list[dict] = read_users()
    for user in users:
        if user["id"] == str(id):
            return user
    return None
