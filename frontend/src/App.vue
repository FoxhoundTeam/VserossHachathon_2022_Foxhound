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
        <v-container justify-end class="pa-0 ma-0 fill-height">
          <!-- TODO исправить, чтобы было видно только для авторизованных -->
          <!-- v-if="$store.state.token" -->

          <v-divider vertical class="mx-2 fill-height"></v-divider>

          <v-avatar color="white">
            <v-icon color="primary"> mdi-account-circle </v-icon>
          </v-avatar>

          <div class="px-4">
            <span class="text-2xl text-white font-semibold">
              Имя пользователя
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
      permanent expand-on-hover dark app clipped mini-variant>
      <!-- сделать видимым только если пользователь авторизован -->
      <!-- v-if="
        this.$store.state.token &&
        this.$store.state.current_user &&
        this.$store.state.current_user.first_name
      " -->

      <v-list nav >
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
    <v-main style="height: 100vh">
      <!-- страницы приложения -->
      <v-container fluid fill-height>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {};
  },

  methods: {
    logout() {
      //
    },
  },

  mounted() {
    //
  },

  computed: {
    //
  },
};
</script>

<style>
.leaflet-attribution-flag {
	display: none;
  visibility: hidden;
}
</style>

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
