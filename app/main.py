"""应用入口：创建 FastAPI 实例、挂载路由、启动服务"""

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from routes import admin, auth

# 把 .env 里的键值加载进环境变量（override=True 表示覆盖已存在的同名变量）
load_dotenv(override=True)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Auth API is running"}


# include_router 把各模块的路由挂到主应用上，
# prefix 会让路由真正暴露在 /api/auth/* 和 /api/admin/*
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


if __name__ == "__main__":
    # python main.py 启动时读 .env 的 PORT（默认 8000）；
    # 与 fastapi dev 不同，uvicorn.run 不会自动读 .env，所以这里手动取
    port = int(os.environ.get("PORT", "8000"))
    # reload=True 提供热重载，等价于 fastapi dev
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
