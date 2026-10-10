import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 前端 /api 请求转发到后端，避免跨域
      "/api": "http://localhost:8080",
    },
  },
});
