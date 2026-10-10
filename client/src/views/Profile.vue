<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api.js";
import { useAuth } from "../auth.js";

const router = useRouter();
const { user, clearToken, isAdmin } = useAuth();

const serverUser = ref(null);
const message = ref("");
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await api.get("/auth/profile");
    serverUser.value = data.user;
  } catch (err) {
    message.value = err.response?.data?.message || "获取失败，请先登录";
  } finally {
    loading.value = false;
  }
});

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
  <div class="card wide">
    <h2>个人资料</h2>
    <p v-if="loading" class="hint">加载中…</p>
    <template v-else-if="serverUser">
      <div class="avatar">{{ serverUser.email?.[0]?.toUpperCase() }}</div>
      <dl class="info">
        <div class="row">
          <dt>邮箱</dt>
          <dd>{{ serverUser.email }}</dd>
        </div>
        <div class="row">
          <dt>角色</dt>
          <dd>
            <span class="badge" :class="isAdmin ? 'badge-admin' : 'badge-user'">
              {{ serverUser.role }}
            </span>
          </dd>
        </div>
        <div class="row">
          <dt>签发时间</dt>
          <dd>{{ new Date(serverUser.iat * 1000).toLocaleString() }}</dd>
        </div>
        <div class="row">
          <dt>过期时间</dt>
          <dd>{{ new Date(serverUser.exp * 1000).toLocaleString() }}</dd>
        </div>
      </dl>
      <div class="actions">
        <RouterLink v-if="isAdmin" to="/admin/users" class="btn btn-outline">用户列表</RouterLink>
        <button class="btn btn-danger" @click="logout">登出</button>
      </div>
    </template>
    <p v-else class="msg msg-error">{{ message }}</p>
  </div>
</template>

<style scoped>
.card.wide {
  max-width: 460px;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  font-size: 24px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.info {
  margin-bottom: 24px;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 14px;
}

.row:last-child {
  border-bottom: none;
}

dt {
  color: var(--text-muted);
}

dd {
  color: var(--text);
  word-break: break-all;
  text-align: right;
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.actions .btn {
  width: auto;
}

.hint {
  text-align: center;
  color: var(--text-muted);
  font-size: 14px;
}
</style>
