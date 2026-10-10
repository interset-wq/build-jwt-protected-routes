<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api.js";

const router = useRouter();
const user = ref(null);
const message = ref("");

onMounted(async () => {
  try {
    const { data } = await api.get("/auth/profile");
    user.value = data.user;
  } catch (err) {
    message.value = err.response?.data?.message || "获取失败，请先登录";
  }
});

async function logout() {
  try {
    await api.post("/auth/logout");
    localStorage.removeItem("token");
    router.push("/login");
  } catch (err) {
    message.value = err.response?.data?.message || "登出失败";
  }
}
</script>

<template>
  <h2>个人资料</h2>
  <p v-if="user">用户信息：{{ JSON.stringify(user, null, 2) }}</p>
  <p class="err">{{ message }}</p>
  <button @click="logout">登出</button>
</template>

<style scoped>
pre-like { white-space: pre-wrap; }
.err { color: red; }
</style>
