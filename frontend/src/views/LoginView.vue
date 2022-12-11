<template>
  <v-container>
    <v-row class="mt-5">
      <v-col cols="12"><h1>FoxInt</h1></v-col>
    </v-row>
    <v-row>
      <v-col class="my-1" sm="7" order-sm="1" order="12">
        <!-- <v-img class="w-50" :src="hackLogo"></v-img> -->
        <h3 class="mt-2">Powered by Foxhound</h3></v-col
      >
      <v-col class="my-1" order-sm="12" order="1" sm="5">
        <login-form />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LoginForm from "../components/LoginForm.vue";
export default {
  components: { LoginForm },
};
</script>

<style>
</style>