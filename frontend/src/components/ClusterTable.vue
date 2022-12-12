<template>
  <v-data-table
    :headers="headers"
    :items="items"
    hide-default-footer
    :items-per-page="-1"
    class="elevation-1"
    fixed-header
    height="80vh"
    :loading="loading"
    must-sort
    :custom-sort="(items) => items"
    @click:row="rowClick(row)"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Кластеры</v-toolbar-title>
        <v-spacer></v-spacer> </v-toolbar
    ></template>
    <template v-slot:[`body.append`] v-if="!loading">
      <v-card v-intersect="fetchData" v-if="!allDataLoaded"></v-card>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: ["items", "loading", "allDataLoaded"],
  data() {
    return {
      headers: [
        {
          text: "Тема",
          align: "start",
          sortable: false,
          value: "theme",
        },
        {
          text: "Кол-во",
          sortable: false,
          value: "articlesCount",
        },
        {
          text: "Регион",
          sortable: false,
          value: "location",
        },
        {
          text: "Тип",
          sortable: false,
          value: "className",
        },
        {
          text: "Дата",
          sortable: false,
          value: "dt",
        },
      ],
    };
  },
  methods: {
    fetchData(entries, observer, isIntersecting) {
      if (this.loading || !isIntersecting) return;
      this.$emit("fetchData");
    },
    rowClick(row) {
      this.$emit("rowClick", row);
    },
  },
  computed: {
    infiniteScrollDisabled() {
      return this.loading || this.allDataLoaded;
    },
  },
};
</script>

<style>
</style>