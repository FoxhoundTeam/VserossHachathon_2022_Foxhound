<template>
  <v-row style="height: 100%" no-gutters fill-height>
    <!-- настройки -->
    <v-col cols="12" md="4" no-gutters class="pa-1">
      <!-- TODO фильтры ввода -->
      <v-text-field
        v-model="ip"
        label="Введите IP-адрес для сканирования"
        outlined
        clearable
        readonly
      ></v-text-field>
      <v-btn color="primary" @click="startScan">
        <v-icon>mdi-magnify-expand</v-icon>
        Сканировать
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import http from "../http";

export default {
  name: "StartScan",

  data() {
    return {
      ip: "158.160.43.251",
    };
  },

  methods: {
    // начать сканирование по адресу
    async startScan() {
      const response = await http.createItem("Scan", {
        showSnackbar: true,
        data: { ip: this.ip },
      });
      if (response.status != 200) return;
      this.$router.replace({
        name: "Сase1View2",
        params: { id: response.data.id },
      });
    },
  },
};
</script>
