# JWT Auth Demo（Express + Vue 3）

基于 JWT 的认证 / 授权演示项目：Express 后端 + Vue 3 前端。

**在线演示**：https://build-jwt-protected-routes.vercel.app

- 后端：Express 5 + jsonwebtoken + bcryptjs + helmet，JSON 文件模拟数据库
- 前端：Vite + Vue 3 + vue-router + axios，token 存 localStorage，拦截器自动携带 Bearer
- 理论与实现讲解见 [docs/jwt.md](docs/jwt.md) 和 [docs/jwt-with-express.md](docs/jwt-with-express.md)

## 功能

| 接口 | 说明 | 权限 |
|---|---|---|
| `POST /api/auth/register` | 注册，成功即签发 JWT | 公开 |
| `POST /api/auth/login` | 登录，签发 JWT | 公开 |
| `POST /api/auth/logout` | 登出，token 加入黑名单 | 登录 |
| `GET /api/auth/profile` | 返回 JWT 解码后的当前用户 | 登录 |
| `GET /api/admin/users` | 用户列表（不含密码哈希） | admin |

## 快速开始

环境要求：Node.js 20+、pnpm

```bash
# 后端（端口 8080）
cd server
pnpm install
pnpm start

# 前端（端口 5173，/api 代理到 8080）
cd client
pnpm install
pnpm dev
```

打开 http://localhost:5173 即可体验。

## 演示账号

| 角色 | 邮箱 | 密码 |
|---|---|---|
| admin | `admin@example.com` | `admin123` |
| user | `admin@test.com` | `123456` |

用 admin 账号登录可访问「用户列表」页，体验基于角色的授权（authorize 中间件）。

## 目录结构

```
├── server/          # Express 后端
│   ├── index.js
│   ├── routes/      # auth.js / admin.js
│   ├── middleware/  # authenticate.js / authorize.js
│   ├── utils/       # db.js / jwt.js / token-blacklist.js
│   └── data/        # users.json（模拟数据库）
├── client/          # Vue 3 前端
│   └── src/
│       ├── views/   # Home / Register / Login / Profile / AdminUsers
│       ├── api.js   # axios 实例 + 拦截器
│       └── auth.js  # 前端登录态管理
└── docs/            # JWT 原理与实现讲解（博文素材）
```

## 安全说明

此项目仅用于教学演示：token 存 localStorage 有 XSS 风险，黑名单存内存重启即失效，生产环境请改用 httpOnly Cookie + 持久化黑名单（或直接用短生命周期 access token + refresh token）。
