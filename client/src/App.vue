<script setup>
</script>

<template>
  <nav>
    <RouterLink to="/">首页</RouterLink>
    <RouterLink to="/register">注册</RouterLink>
    <RouterLink to="/login">登录</RouterLink>
    <RouterLink to="/profile">个人资料</RouterLink>
    <RouterLink to="/admin/users">用户列表</RouterLink>
  </nav>
  <RouterView />
</template>

<style scoped>
nav { display: flex; gap: 16px; padding: 12px; border-bottom: 1px solid #eee; margin-bottom: 16px; }
</style>
