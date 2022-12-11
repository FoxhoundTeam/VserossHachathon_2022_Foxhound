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
      ></v-text-field>
      <v-btn color="primary" @click="startScan" :loading="loading">
        <v-icon v-if="!loading">mdi-magnify-expand</v-icon>
        Сканировать
      </v-btn>
      <v-progress-linear v-if="progress" v-model="progress" height="25">
        <template v-slot:default="{ value }">
          <strong>{{ Math.ceil(value) }}%</strong>
        </template>
      </v-progress-linear>
    </v-col>

    <!-- результаты пентеста -->
    <v-col cols="12" md="8" no-gutters class="pa-1">
      <!-- текстовый лог -->
      <v-virtual-scroll
        ref="log"
        v-model="scan.log"
        label="Лог пентеста"
        outlined
        height="100"
        item-height="20"
      ></v-virtual-scroll>

      <v-card v-if="services">
        <v-card-title>Найденные сервисы</v-card-title>
        <v-data-table :headers="headers" :items="services">
          <template v-slot:[`item.meta`]="{ item }">
            <pre>{{ item.meta }}</pre>
          </template>
        </v-data-table>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import http from "../http";

export default {
  name: "Case1View2",

  data() {
    return {
      headers: [
        { text: "Порт", sortable: false, value: "port" },
        { text: "Название", value: "name" },
        { text: "Продукт", value: "product" },
        { text: "Протокол", value: "proto" },
        { text: "Статус", value: "status" },
        { text: "Версия", value: "version" },
        { text: "Доп. информация", value: "meta" },
      ],
      ip: "",
      longPoolingInterval: null,
      services: null,
      scan: {
        progress: 0,
        log: "aasdsadfsasd "
      },
    };
  },
  computed: {
    loading() {
      return this.scan.status == "running";
    },
    progress() {
      return this.scan.progress * 100;
    },
  },

  methods: {
    async checkStatus() {
      this.scan = (
        await http.getItem("Scan", {
          id: this.scan.id,
          showSnackbar: true,
        })
      ).data;
      this.$refs.log.scrollTop = this.$refs.log.scrollHeight;
      if (this.loading) return;
      clearInterval(this.longPoolingInterval);
      this.services = (
        await http.getItem(`/api/scans/${this.scan.id}/services/`, {
          showSnackbar: true,
        })
      ).data;
    },

    beforeDestroy() {
      clearInterval(this.longPoolingInterval);
    },

    // начать сканирование по адресу
    async startScan() {
      const response = await http.createItem("Scan", {
        showSnackbar: true,
        data: { ip: this.ip },
      });
      if (response.status != 200) return;
      this.scan = response.data;
      if (this.longPoolingInterval == null)
        this.longPoolingInterval = setInterval(this.checkStatus, 2000);
    },
  },
};
</script>
