<script setup>
import { useAuth } from "../auth.js";

const { isLoggedIn, isAdmin } = useAuth();
</script>

<template>
  <div class="hero">
    <h1>JWT 认证 / 授权演示</h1>
    <p class="desc">
      Express + jsonwebtoken 后端，Vue 3 前端。登录后 token 保存在
      localStorage，axios 拦截器自动携带 <code>Authorization: Bearer</code>。
    </p>

    <div v-if="!isLoggedIn" class="cta">
      <RouterLink to="/register" class="btn btn-primary cta-btn">免费注册</RouterLink>
      <RouterLink to="/login" class="btn btn-outline cta-btn">登录</RouterLink>
    </div>

    <div v-else class="cta">
      <RouterLink to="/profile" class="btn btn-primary cta-btn">查看个人资料</RouterLink>
      <RouterLink v-if="isAdmin" to="/admin/users" class="btn btn-outline cta-btn">
        用户列表（Admin）
      </RouterLink>
    </div>

    <div class="card demo-account">
      <h3>演示账号</h3>
      <div class="row">
        <span class="badge badge-admin">admin</span>
        <code>admin@example.com</code> / <code>admin123</code>
      </div>
      <div class="row">
        <span class="badge badge-user">user</span>
        <code>admin@test.com</code> / <code>123456</code>
      </div>
      <p class="note">用 admin 账号登录可访问「用户列表」，体验角色授权。</p>
    </div>
  </div>
</template>

<style scoped>
.hero {
  text-align: center;
  padding: 48px 0 32px;
}

h1 {
  font-size: 28px;
  margin-bottom: 12px;
}

.desc {
  color: var(--text-muted);
  max-width: 560px;
  margin: 0 auto 28px;
  line-height: 1.7;
  font-size: 15px;
}

code {
  background: #eef1f8;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.cta {
  display: flex;
  gap: 14px;
  justify-content: center;
  margin-bottom: 36px;
}

.cta-btn {
  width: auto;
  min-width: 140px;
}

.demo-account {
  max-width: 420px;
  text-align: left;
  margin-top: 0;
  padding: 24px;
}

.demo-account h3 {
  font-size: 15px;
  margin-bottom: 14px;
}

.demo-account .row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
  font-size: 14px;
}

.note {
  margin-top: 12px;
  font-size: 13px;
  color: var(--text-muted);
}
</style>
