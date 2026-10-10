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
const isError = ref(false);
const loading = ref(false);

async function register() {
  message.value = "";
  loading.value = true;
  try {
    const { data } = await api.post("/auth/register", {
      email: email.value,
      password: password.value,
    });
    setToken(data.token);
    message.value = data.message + "，正在跳转…";
    setTimeout(() => router.push("/profile"), 600);
  } catch (err) {
    isError.value = true;
    message.value = err.response?.data?.message || "注册失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="card">
    <h2>注册</h2>
    <form @submit.prevent="register">
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
            placeholder="至少 6 位密码"
            required
            minlength="6"
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
        {{ loading ? "注册中…" : "注 册" }}
      </button>
    </form>
    <p v-if="message" class="msg" :class="isError ? 'msg-error' : 'msg-success'">{{ message }}</p>
    <p class="switch-tip">已有账号？<RouterLink to="/login">直接登录</RouterLink></p>
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
