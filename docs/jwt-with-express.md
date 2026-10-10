# 在Express中实现JWT

## 依赖

```bash
npm install bcryptjs jsonwebtoken
```

- bcryptjs 用于密码哈希化，比对密码和哈希化的密码
- jsonwebtoken 签发和验证JWT

## 项目结构

```
.
├── data                   # 通过JSON模拟DB
│   └── users.json
├── index.js
├── middleware             # 鉴权中间件
│   ├── authenticate.js    # 登录
│   └── authorize.js       # 授权
├── package.json
├── package-lock.json
├── .env                   # 用于存放JWT_SECRET
├── routes                 # 路由
│   ├── admin.js
│   └── auth.js            # 登录
└── utils                  # 工具
    ├── db.js              # 数据库CRUD
    ├── jwt.js             # 封装jsonwebtoken库实现JWT的签发和验证
    └── token-blacklist.js
```

## .env

```
PORT=8080
JWT_SECRET=some_long_jwt_secret_key # 用于生成JWT的signature
```

## utils/

### db.js

读写JSON文件模拟数据库CRUD操作

```js
import fs from "fs";
import path from "path";

// ES6 没有内置的_dirname常量
const DB_PATH = path.join(import.meta.dirname, "../data/users.json");

// READ
export function readUsers() {
  const data = fs.readFileSync(DB_PATH, "utf-8").trim();
  if (!data) return [];
  return JSON.parse(data);
}

// CREATE
export function writeUsers(users) {
  fs.writeFileSync(DB_PATH, JSON.stringify(users, null, 2));
}

// READ by email
export function findByEmail(email) {
  return readUsers().find((u) => u.email === email) || null;
}

// READ by ID
export function findById(id) {
  return readUsers().find((u) => u.id === id) || null;
}
```

### jwt.js

封装jsonwebtoken库，用于签发和验证JWT

JWT `header.payload.signature`

- header：base64编码，保存加密算法等（由jwt库自动传入）
- payload：base64编码，保存实际的json数据
- signature: 由header、payload、secret-key通过加密算法生成

```js
import jwt from "jsonwebtoken";

// 签发，JWT有效期1天
export function signToken(payload) {
  return jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: "1d" });
}

// 验证Token是否有效，token有效则解码payload
export function verifyToken(token) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch {
    return null;
  }
}
```

### token-blacklist.js

将登出用户的token加入黑名单

用户登出之后，但是token仍在有效期之内。此时应该认为已登出用户的token是无效的token。

```js
const blacklist = new Set();

export function blacklistToken(token) {
  blacklist.add(token);
}

export function isBlacklisted(token) {
  return blacklist.has(token);
}
```

## routes/

User: id(UUID), email, passwordHash, role(user)

### auth.js

- POST /register
- POST /login
- POST /logout 需要鉴权
- GET /profile 需要鉴权

因为登出和查看个人信息的前提是已登录

```js
import express from "express";
import bcrypt from "bcryptjs";
import { randomUUID } from "crypto";

import { findByEmail, readUsers, writeUsers } from "../utils/db.js";
import { signToken } from "../utils/jwt.js";
import authenticate from "../middleware/authenticate.js";
import { blacklistToken } from "../utils/token-blacklist.js";

const router = express.Router();

// POST /register 注册成功后马上签发一个JWT
router.post("/register", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res
        .status(400)
        .json({ message: "Email and password are required" });
    }

    if (findByEmail(email)) {
      return res.status(409).json({ message: "Email already in use" });
    }

    const passwordHash = await bcrypt.hash(password, 10);
    const users = readUsers();
    const newUser = {
      id: randomUUID(),
      email,
      passwordHash,
      provider: "local",
      role: "user",
    };

    users.push(newUser);
    writeUsers(users);

    const token = signToken({
      id: newUser.id,
      email: newUser.email,
      role: newUser.role,
    });
    res.status(201).json({ message: "User registered successfully", token });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// POST /login 登录成功签发JWT
router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res
        .status(400)
        .json({ message: "Email and password are required" });
    }

    const user = findByEmail(email);
    if (!user) {
      return res.status(401).json({ message: "Invalid credentials" });
    }

    const match = await bcrypt.compare(password, user.passwordHash);
    if (!match) {
      return res.status(401).json({ message: "Invalid credentials" });
    }

    const token = signToken({
      id: user.id,
      email: user.email,
      role: user.role,
    });
    res.json({ message: "Login successful", token });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// POST /logout
router.post("/logout", authenticate, (req, res) => {
  const token = req.headers.authorization.split(" ")[1];
  blacklistToken(token);
  res.json({ message: "Logged out successfully" });
});

router.get("/profile", authenticate, (req, res) => {
  res.json({ user: req.user });
});

export default router;
```

### admin.js

- GET /users 需要鉴权和授权，这是admin才能使用的路由

```js
import express from "express";
import authenticate from "../middleware/authenticate.js";
import authorizeRole from "../middleware/authorize.js";
import { readUsers } from "../utils/db.js";

const router = express.Router();

router.get("/users", authenticate, authorizeRole("admin"), (req, res) => {
  const users = readUsers().map(({ passwordHash, ...user }) => user);
  res.json({ users });
});

export default router;
```

## middleware/ 鉴权中间件

### authenticate.js

客户端通过 Bearer 认证方案，在 Authorization 请求头中发送令牌：`Authorization: Bearer <token>`


```js
import { verifyToken } from "../utils/jwt.js";
import { isBlacklisted } from "../utils/token-blacklist.js";

// 鉴权：校验token，有效则解码
export default function authenticate(req, res, next) {
  // 获取headers中的Authorization
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ message: "No token provided" });
  }

  const token = authHeader.split(" ")[1];

  if (isBlacklisted(token)) {
    return res
      .status(401)
      .json({ message: "Token has been invalidated. Log in again." });
  }

  const decoded = verifyToken(token);

  if (!decoded) {
    return res.status(401).json({ message: "Invalid or expired token" });
  }

  req.user = decoded;
  next();
}
```

### authorize.js

授权

```js
export default function authorizeRole(role) {
  return (req, res, next) => {
    if (!req.user || req.user.role !== role) {
      return res.status(403).json({ message: "Access denied" });
    }
    next();
  };
}
```

## index.js

```js
import express from "express";
import helmet from "helmet";

import authRoutes from "./routes/auth.js";
import adminRoutes from "./routes/admin.js";

const PORT = process.env.PORT;
const app = express();

app.use(helmet());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({ message: "Auth API is running" });
});

app.use("/api/auth", authRoutes);
app.use("/api/admin", adminRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}...`);
});
```

## 其他中间件

```js
app.use(helmet());
app.use(express.json());
```

### helmet

- 防止点击劫持（X-Frame-Options），禁止页面被 iframe 嵌入
- 开启XSS 防护（X-XSS-Protection）
- 阻止 MIME 类型嗅探（X-Content-Type-Options）
- 设置内容安全策略 CSP（Content-Security-Policy）
- 隐藏 X-Powered-By: 不让攻击者知道后端是 Express
- 强制 HTTPS
- 还有 Referrer-Policy、Permissions-Policy 等一系列安全头

### express.json() 

Express 内置中间件，作用：解析请求体里的 JSON 格式数据，解析完成后把数据放到 req.body。

前端发 Content-Type: application/json 的请求（axios /fetch post json），后端要拿到传过来的 json 对象，就需要它。