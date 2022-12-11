import Vue from "vue";
import VueRouter from "vue-router";
import Case1View1 from "../views/Case1View1.vue";
import Case1View2 from "../views/Case1View2.vue";
import Case2View from "../views/Case2View.vue";
import LoginView from "../views/LoginView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "LoginView",
    component: LoginView,
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/",
    name: "Сase1View1",
    component: Case1View1,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/scan",
    name: "Сase1View2",
    component: Case1View2,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/case2",
    name: "Case2View",
    component: Case2View,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = new VueRouter({
  routes,
});

export default router;
