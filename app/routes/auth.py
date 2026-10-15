"""
认证路由：register / login / logout / profile
对标 server/routes/auth.js
"""

from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

from pwdlib.hashers.bcrypt import BcryptHasher

from deps import CurrentUser, Token
from utils.db import read_by_email, read_users, write_users
from utils.jwt import sign_token
from utils.token_blacklist import blacklist_token

# 密码哈希工具实例：注册时 password_hash.hash(明文) 生成哈希存库，
# 登录时 password_hash.verify(明文, 库里的哈希) 校验密码，全程不碰明文存储。
# pwdlib 支持多种算法，PasswordHash(哈希器元组) 指定用哪种——
# 这里显式选 BcryptHasher，因为 users.json 里已有用户的哈希是 Express 端
# bcryptjs 生成的（$2b$ 开头）；pwdlib 默认的 argon2 认不出这种格式，
# 不显式指定的话老用户会全部登录失败。
password_hash = PasswordHash((BcryptHasher(),))

router = APIRouter(prefix="/auth", tags=["auth"])


class Credentials(BaseModel):
    """JSON 请求体模型。

    它本身只是个 Pydantic 数据类，"自动校验"由 FastAPI 触发：
    路由函数参数标注了 body: Credentials，FastAPI 在进入函数前会把
    客户端发来的 JSON 构造成 Credentials 实例，字段缺失/类型不符则
    拦截请求并自动返回 422（带具体错误位置），函数内拿到的 body
    已保证字段齐全、类型正确。
    """

    email: str
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: Credentials) -> dict:
    """注册：创建用户并立即签发 JWT（注册成功即登录）"""
    # 422 校验已由 Credentials 保证字段存在，这里兜底空字符串
    if not body.email or not body.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    if read_by_email(body.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use",
        )

    # 密码只存哈希不存明文；provider 表示登录方式（预留第三方登录），
    # role 用于后续 admin 接口的授权判断
    new_user = {
        "id": str(uuid4()),
        "email": body.email,
        "passwordHash": password_hash.hash(body.password),
        "provider": "local",
        "role": "user",
    }
    users = read_users()
    users.append(new_user)
    write_users(users)

    # JWT 的 payload 只放身份信息（不放密码），客户端每次请求带上它，
    # 服务端解码即可知道"是谁、什么角色"，无需查库
    token = sign_token(
        {"id": new_user["id"], "email": new_user["email"], "role": new_user["role"]}
    )
    return {"message": "User registered successfully", "token": token}


@router.post("/login")
def login(body: Credentials) -> dict:
    """登录：校验密码，成功则签发 JWT"""
    # 短路求值：用户不存在时不会执行 verify，统一返回同一个错误信息，
    # 不区分"用户不存在"和"密码错误"，避免暴露某邮箱是否已注册
    user = read_by_email(body.email)
    if not user or not password_hash.verify(body.password, user["passwordHash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = sign_token(
        {"id": user["id"], "email": user["email"], "role": user["role"]}
    )
    return {"message": "Login successful", "token": token}


@router.post("/logout")
def logout(token: Token, user: CurrentUser) -> dict:
    """登出：把当前 token 加入黑名单使其立即失效。

    JWT 本身是无状态的、签发后在有效期内一直有效，服务端无法"删除"它；
    黑名单是让 token 提前作废的常见手段。两个依赖参数分工：
    CurrentUser 保证"必须先登录"，Token 拿原始 token 字符串去拉黑。
    """
    blacklist_token(token)
    return {"message": "Logged out successfully"}


@router.get("/profile")
def profile(user: CurrentUser) -> dict:
    """当前登录用户信息：user 是 JWT 解码后的 payload（见 deps.get_current_user）"""
    return {"user": user}


@router.post("/token")
def token_for_docs(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    """表单格式登录端点，供 Swagger Authorize 弹窗使用（OAuth2 密码流）。

    前端正常走 /login（JSON）即可，此端点仅为 /docs 的调试流程服务。
    """
    user = read_by_email(form.username)
    if not user or not password_hash.verify(form.password, user["passwordHash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = sign_token(
        {"id": user["id"], "email": user["email"], "role": user["role"]}
    )
    # OAuth2 密码流规定返回 access_token / token_type 字段
    return {"access_token": access_token, "token_type": "bearer"}
