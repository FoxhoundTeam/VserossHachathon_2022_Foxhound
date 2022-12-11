<template>
  <v-app>
    <!-- заголовок -->

    <v-app-bar app color="primary" dark clipped-left>
      <v-app-bar-title class="mt-1">
        <h2 justify-start>FoxInt</h2>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <!-- иконка пользователя и кнопка выхода, видны только для авторизованных пользователей -->

      <div justify-end class="pa-0 ma-0 fill-height">
        <v-container justify-end class="pa-0 ma-0 fill-height" v-if="isAuthenticated">

          <v-divider vertical class="mx-2 fill-height"></v-divider>

          <v-avatar color="white">
            <v-icon color="primary"> mdi-account-circle </v-icon>
          </v-avatar>

          <div class="px-4">
            <span class="text-2xl text-white font-semibold">
              {{ user.email }}
            </span>
          </div>

          <v-divider inset vertical class="mx-2"></v-divider>

          <v-btn outlined @click="logout"> Выход </v-btn>
        </v-container>
      </div>
    </v-app-bar>

    <!-- меню навигации по интерфейсу -->
    <v-navigation-drawer
      class="pa-0"
      permanent
      expand-on-hover
      dark
      app
      clipped
      mini-variant
      v-if="isAuthenticated"
    >
      <!-- сделать видимым только если пользователь авторизован -->
      <!-- v-if="
        this.$store.state.token &&
        this.$store.state.current_user &&
        this.$store.state.current_user.first_name
      " -->

      <v-list nav>
        <v-list-item @click="$router.replace({ name: 'Сase1View1' })">
          <!-- v-if="this.$store.state.current_user && this.$store.state.current_user.groups[0]>=4" -->
          <v-list-item-icon>
            <v-icon>mdi-compass-rose</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title
              >Задача 1.<br />Открытые источники</v-list-item-title
            >
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="$router.replace({ name: 'Сase1View2' })">
          <!-- v-if="this.$store.state.current_user && this.$store.state.current_user.groups[0]>=4" -->
          <v-list-item-icon>
            <v-icon>mdi-sunglasses</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Задача 1.<br />Сканирование</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="$router.replace({ name: 'Case2View' })">
          <!-- v-if="this.$store.state.current_user && this.$store.state.current_user.groups[0]>=4" -->
          <v-list-item-icon>
            <v-icon>mdi-target-variant</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Задача 2</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-dialog v-model="showErrorModalLocal" max-width="300">
      <v-card>
        <v-card-title class="text-h5"> Ошибка </v-card-title>

        <v-card-text>
          {{ errorModalContent }}
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="green darken-1"
            text
            @click="showErrorModalLocal = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar
      v-model="showSnackbarLocal"
      :color="snackbarColor || 'success'"
      :timeout="2000"
    >
      {{ snackbarText }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="white"
          text
          v-bind="attrs"
          @click="showSnackbarLocal = false"
        >
          Закрыть
        </v-btn>
      </template>
    </v-snackbar>
    <v-main style="height: 100vh">
      <!-- страницы приложения -->
      <v-container fluid fill-height>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapMutations, mapState } from "vuex";
export default {
  methods: {
    ...mapMutations(["setShowSnackbar", "setShowErrorModal"]),
    async logout() {
      await this.$store.dispatch("logout");
      location.reload();
    },
  },
  computed: {
    ...mapState([
      "snackbarText",
      "showSnackbar",
      "snackbarColor",
      "showErrorModal",
      "errorModalContent",
      "isAuthenticated",
      "user",
    ]),
    showSnackbarLocal: {
      get() {
        return this.showSnackbar;
      },
      set(value) {
        this.setShowSnackbar(value);
      },
    },
    showErrorModalLocal: {
      get() {
        return this.showErrorModal;
      },
      set(value) {
        this.setShowErrorModal(value);
      },
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
