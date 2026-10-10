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
