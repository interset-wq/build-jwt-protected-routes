<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api.js";
import { useAuth } from "../auth.js";

const router = useRouter();
const { setToken } = useAuth();

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const message = ref("");
const loading = ref(false);

async function login() {
  message.value = "";
  loading.value = true;
  try {
    const { data } = await api.post("/auth/login", {
      email: email.value,
      password: password.value,
    });
    setToken(data.token);
    router.push("/profile");
  } catch (err) {
    message.value = err.response?.data?.message || "登录失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="card">
    <h2>登录</h2>
    <form @submit.prevent="login">
      <div class="field">
        <label>邮箱</label>
        <input v-model="email" type="email" placeholder="you@example.com" required />
      </div>
      <div class="field">
        <label>密码</label>
        <div class="pwd-wrap">
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="密码"
            required
          />
          <button
            type="button"
            class="pwd-toggle"
            :title="showPassword ? '隐藏密码' : '显示密码'"
            @click="showPassword = !showPassword"
          >
            {{ showPassword ? "隐藏" : "显示" }}
          </button>
        </div>
      </div>
      <button class="btn btn-primary" type="submit" :disabled="loading">
        {{ loading ? "登录中…" : "登 录" }}
      </button>
    </form>
    <p v-if="message" class="msg msg-error">{{ message }}</p>
    <p class="switch-tip">还没有账号？<RouterLink to="/register">免费注册</RouterLink></p>
  </div>
</template>

<style scoped>
.switch-tip {
  margin-top: 18px;
  font-size: 14px;
  color: var(--text-muted);
  text-align: center;
}

.switch-tip a {
  color: var(--primary);
  text-decoration: none;
}
</style>
