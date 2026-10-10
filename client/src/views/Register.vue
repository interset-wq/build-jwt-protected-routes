<script setup>
import { ref } from "vue";
import api from "../api.js";

const email = ref("");
const password = ref("");
const message = ref("");
const error = ref(false);

async function register() {
  message.value = "";
  try {
    const { data } = await api.post("/auth/register", {
      email: email.value,
      password: password.value,
    });
    localStorage.setItem("token", data.token);
    message.value = data.message + "（已自动登录）";
  } catch (err) {
    error.value = true;
    message.value = err.response?.data?.message || "注册失败";
  }
}
</script>

<template>
  <h2>注册</h2>
  <form @submit.prevent="register">
    <input v-model="email" type="email" placeholder="邮箱" required />
    <input v-model="password" type="password" placeholder="密码" required />
    <button type="submit">注册</button>
  </form>
  <p :class="{ err: error }">{{ message }}</p>
</template>

<style scoped>
form { display: flex; flex-direction: column; gap: 10px; max-width: 300px; }
input, button { padding: 8px; }
.err { color: red; }
</style>
