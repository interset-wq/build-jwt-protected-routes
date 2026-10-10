<script setup>
import { ref, onMounted } from "vue";
import api from "../api.js";

const users = ref([]);
const message = ref("");
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await api.get("/admin/users");
    users.value = data.users;
  } catch (err) {
    message.value = err.response?.data?.message || "获取失败（需要 admin 权限）";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="page">
    <h2>用户列表</h2>
    <p class="sub">需要 admin 角色（authorize 中间件保护）</p>
    <p v-if="loading" class="hint">加载中…</p>
    <p v-else-if="message" class="msg msg-error">{{ message }}</p>
    <table v-else class="table">
      <thead>
        <tr>
          <th>邮箱</th>
          <th>角色</th>
          <th>ID</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.email }}</td>
          <td>
            <span class="badge" :class="u.role === 'admin' ? 'badge-admin' : 'badge-user'">
              {{ u.role }}
            </span>
          </td>
          <td class="mono">{{ u.id }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.page {
  margin: 32px 0;
}

h2 {
  margin-bottom: 4px;
}

.sub {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.hint {
  color: var(--text-muted);
  font-size: 14px;
}

.mono {
  font-family: Consolas, monospace;
  font-size: 12px;
  color: var(--text-muted);
}
</style>
