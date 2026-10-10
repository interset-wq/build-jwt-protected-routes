import { createRouter, createWebHistory } from "vue-router";

import Home from "./views/Home.vue";
import Register from "./views/Register.vue";
import Login from "./views/Login.vue";
import Profile from "./views/Profile.vue";
import AdminUsers from "./views/AdminUsers.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/profile", component: Profile },
  { path: "/admin/users", component: AdminUsers },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
