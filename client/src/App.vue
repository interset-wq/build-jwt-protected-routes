<script setup>
import { useRouter } from "vue-router";
import { useAuth } from "./auth.js";
import api from "./api.js";

const router = useRouter();
const { isLoggedIn, isAdmin, clearToken } = useAuth();

async function logout() {
  try {
    await api.post("/auth/logout");
  } catch {
    // token 已失效也无需阻断登出
  }
  clearToken();
  router.push("/login");
}
</script>

<template>
  <header class="header">
    <RouterLink to="/" class="brand">JWT Auth Demo</RouterLink>
    <nav class="nav">
      <template v-if="isLoggedIn">
        <RouterLink v-if="isAdmin" to="/admin/users" class="nav-link">用户列表</RouterLink>
        <RouterLink to="/profile" class="nav-link">个人资料</RouterLink>
        <button class="nav-link btn-logout" @click="logout">登出</button>
      </template>
      <template v-else>
        <RouterLink to="/register" class="nav-link">注册</RouterLink>
        <RouterLink to="/login" class="nav-link">登录</RouterLink>
      </template>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 8px;
}

.brand {
  font-weight: 700;
  font-size: 18px;
  color: var(--primary);
  text-decoration: none;
}

.nav {
  display: flex;
  align-items: center;
  gap: 18px;
}

.nav-link {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-family: inherit;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary);
}

.btn-logout {
  color: var(--danger);
}
</style>
