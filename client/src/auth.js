import { ref, computed } from "vue";

const token = ref(localStorage.getItem("token"));

// 简易解码 JWT payload（base64url）
function decodePayload(t) {
  try {
    return JSON.parse(atob(t.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
  } catch {
    return null;
  }
}

export function useAuth() {
  const user = computed(() => (token.value ? decodePayload(token.value) : null));
  const isLoggedIn = computed(() => !!user.value);
  const isAdmin = computed(() => user.value?.role === "admin");

  function setToken(t) {
    token.value = t;
    localStorage.setItem("token", t);
  }

  function clearToken() {
    token.value = null;
    localStorage.removeItem("token");
  }

  return { token, user, isLoggedIn, isAdmin, setToken, clearToken };
}
