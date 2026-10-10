<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api.js";

const router = useRouter();
const email = ref("");
const password = ref("");
const message = ref("");

async function login() {
  message.value = "";
  try {
    const { data } = await api.post("/auth/login", {
      email: email.value,
      password: password.value,
    });
    localStorage.setItem("token", data.token);
    router.push("/profile");
  } catch (err) {
    message.value = err.response?.data?.message || "登录失败";
  }
}
</script>

<template>
  <h2>登录</h2>
  <form @submit.prevent="login">
    <input v-model="email" type="email" placeholder="邮箱" required />
    <input v-model="password" type="password" placeholder="密码" required />
    <button type="submit">登录</button>
  </form>
  <p class="err">{{ message }}</p>
</template>

<style scoped>
form { display: flex; flex-direction: column; gap: 10px; max-width: 300px; }
input, button { padding: 8px; }
.err { color: red; }
</style>
