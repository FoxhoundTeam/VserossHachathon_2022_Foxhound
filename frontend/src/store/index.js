import Vuex from "vuex";
import http from "../http";
import Vue from "vue";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null,
    isAuthenticated: false,
    showErrorModal: false,
    errorModalContent: null,
    snackbarColor: null,
    showSnackbar: false,
    snackbarText: null,
  },
  getters: {},
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setAuthenticated(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    showErrorModal(state, content) {
      state.errorModalContent = content;
      state.showErrorModal = true;
    },
    setShowErrorModal(state, value) {
      state.showErrorModal = value;
    },
    showSnackbar(state, content) {
      state.snackbarColor = content.color || "success";
      state.snackbarText = content.text;
      state.showSnackbar = true;
    },
    setShowSnackbar(state, value) {
      state.showSnackbar = value;
    },
  },
  actions: {
    async login(context, credentials) {
      const response = await http.createItem("Login", {
        data: credentials,
        showSnackbar: true,
      });
      if (response.status == 200) {
        localStorage.setItem("accessToken", response.data.accessToken);
      }
      await context.dispatch("checkAuth");
    },
    async logout(context) {
      localStorage.removeItem("accessToken");
      context.commit("setAuthenticated", false);
      context.commit("setUser", {});
    },
    async register(context, credentials) {
      const response = await http.createItem("Register", {
        data: credentials,
        showSnackbar: true,
      });
      let registered = false;
      if (response.status == 201) {
        localStorage.setItem("accessToken", response.data.accessToken);
        registered = true;
      }
      await context.dispatch("checkAuth");
      return registered;
    },
    async checkAuth(context) {
      const result = await http.getItem("User");
      if (result.status != 200) {
        context.commit("setUser", {});
      } else {
        context.commit("setAuthenticated", true);
        context.commit("setUser", result.data);
      }
    },
  },
});
