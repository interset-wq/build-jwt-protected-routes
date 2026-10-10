import usersData from "../data/users.json" with { type: "json" };

// Vercel 等 serverless 环境的文件系统是只读的，
// 用户数据只能在内存中读写，实例重启后丢失（本地 dev 除外）
const users = [...usersData];

// READ all
export function readUsers() {
  return users;
}

// CREATE / WRITE（传入的数组可能就是内存数组本身，此时无需拷贝）
export function writeUsers(updated) {
  if (updated === users) return;
  users.length = 0;
  users.push(...updated);
}

// READ by email
export function findByEmail(email) {
  return users.find((u) => u.email === email) || null;
}

// READ by ID
export function findById(id) {
  return users.find((u) => u.id === id) || null;
}
