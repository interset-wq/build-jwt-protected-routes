"""
依赖注入：鉴权（authenticate）与授权（authorize_role）
相当于 Express 中间件
对标 server/middleware/authenticate.js 和 authorize.js

依赖注入（DI）速览：路由参数标注 Annotated[类型, Depends(fn)] 时，
FastAPI 会在进入路由函数前自动调用 fn，把返回值作为该参数传入——
相当于 Express 里"先跑中间件、再进 handler"，但声明在参数上更直观。

关于 OAuth2PasswordBearer：
- 它只负责从 Authorization: Bearer <token> 提取 token，本身不做任何校验，
  校验仍由 verify_token + 黑名单完成；
- token 缺失时自动返回 401（带 WWW-Authenticate: Bearer 头）；
- tokenUrl 是给 /docs 的 Swagger 文档看的元信息（Authorize 按钮），
  指向签发 token 的接口。Swagger 的 Authorize 弹窗按 OAuth2 密码流
  发 form 表单，因此 routes/auth.py 专门提供了表单格式的 /token 端点
  供它调用；前端正常走 /login（JSON）即可。
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from utils.jwt import verify_token
from utils.token_blacklist import is_blacklisted

# tokenUrl 指向签发 token 的接口，仅供 Swagger 文档展示
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# ==================== 手动实现版本（保留备用） ====================
# 不依赖 fastapi.security，直接解析 Authorization 头，与 OAuth2PasswordBearer 版本二选一使用。

# def get_current_user(request: Request) -> dict:
#     """手动版鉴权：校验 Authorization: Bearer <token>，有效则返回解码后的 payload"""
#     auth_header = request.headers.get("Authorization", "")
#     if not auth_header.startswith("Bearer "):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="No token provided",
#         )
#     token = auth_header.split(" ")[1]
#     if is_blacklisted(token):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has been invalidated. Log in again.",
#         )
#     decoded = verify_token(token)
#     if not decoded:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#         )
#     return decoded

# ==================== OAuth2PasswordBearer 版本（当前使用） ====================

def get_current_user(token: Annotated[str, Depends(reusable_oauth2)]) -> dict:
    """核心鉴权依赖：token 有效则返回解码后的 payload（含 id/email/role/exp）。

    依赖可嵌套：参数里的 Depends(reusable_oauth2) 会先执行，拿到原始
    token 字符串，这里再依次做黑名单检查、验签。
    """
    # 已登出的 token 先拦下（黑名单见 utils/token_blacklist.py）
    if is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated. Log in again.",
        )

    # 验签 + 过期校验，任何失败都返回 None（见 utils/jwt.py）
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return decoded


def require_role(role: str):
    """授权依赖的工厂函数：require_role("admin") 返回一个现成的依赖。

    之所以做成工厂，是因为角色是在写路由时才确定的——
    用法：@router.get("/users", dependencies=[Depends(require_role("admin"))])
    对应 Express 的 authorizeRole("admin") 中间件。
    """

    def _authorize(user: Annotated[dict, Depends(get_current_user)]) -> dict:
        """先登录，再授权"""
        if not user or user.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
        return user

    return _authorize


# ---- 常用依赖的短别名，路由参数直接写 user: CurrentUser 即可 ----

# 走完整鉴权链（提取→黑名单→验签），拿解码后的用户信息
CurrentUser = Annotated[dict, Depends(get_current_user)]
# 只提取不校验的原始 token 字符串（logout 加黑名单用）
Token = Annotated[str, Depends(reusable_oauth2)]