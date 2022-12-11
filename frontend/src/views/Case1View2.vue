<template>
  <v-row style="height: 100%" no-gutters fill-height>

    <!-- настройки -->
    <v-col cols="12" md="4" no-gutters class="pa-1">
      <!-- TODO фильтры ввода -->
      <v-text-field
        v-model="ipaddress"
        label="Введите IP-адрес для сканирования"
        outlined
        clearable
      ></v-text-field>
      <v-btn color="primary" @click="scan" :loading="is_scanning">
        <v-icon v-if="!is_scanning">mdi-magnify-expand</v-icon>
        Сканировать
      </v-btn>
    </v-col>

    <!-- результаты пентеста -->
    <v-col cols="12" md="8" no-gutters class="pa-1">
      <!-- текстовый лог -->
      <v-textarea
        v-model="process_log"
        label="Лог пентеста"
        outlined
        readonly
      ></v-textarea>

      <!-- извлечённые файлы -->
      <v-card>
        <v-card-title>Извлечённые файлы</v-card-title>
        <v-data-table>
          
        </v-data-table>
      </v-card>
      

    </v-col>
  </v-row>
</template>

<script>
// @ is an alias to /src


export default {
  name: 'Case1View2',

  data() {
    return {
      is_scanning : false,
      process_log : "",
    }
  },

  methods:{
    // начать сканирование по адресу
    scan(){
      this.is_scanning = true;
    }
  }
}
</script>
