import fs from "fs";
import path from "path";

// ES6 没有内置的__dirname常量
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
