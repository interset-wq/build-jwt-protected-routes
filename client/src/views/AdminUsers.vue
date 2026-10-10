<script setup>
import { ref, onMounted } from "vue";
import api from "../api.js";

const users = ref([]);
const message = ref("");

onMounted(async () => {
  try {
    const { data } = await api.get("/admin/users");
    users.value = data.users;
  } catch (err) {
    message.value = err.response?.data?.message || "获取失败（需要 admin 权限）";
  }
});
</script>

<template>
  <h2>用户列表（Admin）</h2>
  <p class="err">{{ message }}</p>
  <table v-if="users.length">
    <thead>
      <tr><th>ID</th><th>邮箱</th><th>角色</th></tr>
    </thead>
    <tbody>
      <tr v-for="u in users" :key="u.id">
        <td>{{ u.id }}</td>
        <td>{{ u.email }}</td>
        <td>{{ u.role }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
table { border-collapse: collapse; }
th, td { border: 1px solid #ccc; padding: 6px 12px; }
.err { color: red; }
</style>
