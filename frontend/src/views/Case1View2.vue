<template>
  <v-row style="height: 100%" no-gutters fill-height>
    <!-- настройки -->
    <v-col cols="12" md="4" no-gutters class="pa-1">
      <p>
        {{ loading ? "Сканируем:" : "Результаты сканирования:" }} {{ scan.ip }}
      </p>
      <v-progress-linear v-model="progress" height="25" class="mt-5">
        <template v-slot:default="{ value }">
          <strong>{{ Math.ceil(value) }}%</strong>
        </template>
      </v-progress-linear>
    </v-col>

    <!-- результаты пентеста -->
    <v-col cols="12" md="8" no-gutters class="pa-1">
      <!-- текстовый лог -->
      <v-card v-if="log" class="mb-4">
        <v-card-title>Лог пентеста</v-card-title>
        <v-virtual-scroll ref="log" height="300" item-height="50" :items="log">
          <template v-slot:default="{ item }">
            <v-list-item>
              {{ item }}
            </v-list-item>
          </template>
        </v-virtual-scroll>
      </v-card>

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
      longPoolingInterval: null,
      services: null,
      scan: {
        progress: 0,
        log: [],
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
    log() {
      return this.scan.log;
    },
  },
  beforeDestroy() {
    clearInterval(this.longPoolingInterval);
  },

  updated() {
    this.$refs.log.$el.scrollTop = this.$refs.log.$el.scrollHeight;
  },

  async beforeMount() {
    this.scan = (
      await http.getItem("Scan", {
        id: this.$route.params.id,
        showSnackbar: true,
      })
    ).data;
    if (this.loading && this.longPoolingInterval == null)
      this.longPoolingInterval = setInterval(this.checkStatus, 2000);
    else if (!this.loading) {
      this.services = (
        await http.getItem(`/api/scans/${this.scan.id}/services/`, {
          showSnackbar: true,
        })
      ).data;
    }
  },

  methods: {
    async checkStatus() {
      this.scan = (
        await http.getItem("Scan", {
          id: this.scan.id,
          showSnackbar: true,
        })
      ).data;
      if (this.loading) return;
      clearInterval(this.longPoolingInterval);
      this.services = (
        await http.getItem(`/api/scans/${this.scan.id}/services/`, {
          showSnackbar: true,
        })
      ).data;
    },
  },
};
</script>
