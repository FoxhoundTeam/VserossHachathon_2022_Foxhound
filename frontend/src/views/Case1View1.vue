<template>
  <v-row style="height: 100%" no-gutters fill-height>

    <!-- таблица кластеров, фильтры, сортировка -->
    <v-col cols="12" md="4" no-gutters class="pa-1">
      <v-row>
        <v-btn color="primary" @click="report" class="ma-1">
          <v-icon>mdi-download</v-icon>
          Отчёт
        </v-btn>
      </v-row>
      <v-row>
        <v-data-table
          :headers="headers"
          :items="clusters"
          :items-per-page="20"
          fill-height
        >
        </v-data-table>
      </v-row>

    </v-col>

    <!-- карта -->
    <v-col cols="12" md="8" no-gutters class="pa-1">
      <l-map
        style="height: 100%;" :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-polygon :lat-lngs="test_polygon" :color="'green'"></l-polygon>

        <!-- https://vue2-leaflet.netlify.app/components/LGeoJson.html#demo -->
        <l-geo-json :geojson="geojson"></l-geo-json>
        <!--  -->
        <!-- <l-marker :lat-lng="markerLatLng"></l-marker> -->
      </l-map>
    </v-col>
  </v-row>
</template>

<script>
// @ is an alias to /src

// import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
// import 'leaflet/dist/leaflet.css';
// import Vue from 'vue';
// Vue.component('l-map', LMap);
// Vue.component('l-tile-layer', LTileLayer);
// Vue.component('l-marker', LMarker);

// import L from 'leaflet';
import axios from "axios";
import {
  LMap,
  LTileLayer /*, LMarker */,
  LPolygon,
  LGeoJson,
} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "Case1View1",

  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LGeoJson,
    // LMarker,
  },

  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [55.751244, 37.618423],

      headers: [
        {
          text: "Тема",
          align: "start",
          sortable: false,
          value: "topic",
        },
        {
          text: "Кол-во",
          value: "number",
        },
        {
          text: "Регион",
          value: "region",
        },
        {
          text: "Тип",
          value: "type",
        },
        {
          text: "Дата",
          value: "date",
        },
      ],
      clusters: [
        {
          topic: ["Лесной", "пожар", "Якутия"],
          number: 15,
          type: "Лесной пожар",
          date: "2022-07-15",
        },
        {
          topic: ["Лесной", "пожар", "Якутия"],
          number: 15,
          type: "Лесной пожар",
          date: "2022-07-15",
        },
        {
          topic: ["Лесной", "пожар", "Якутия"],
          number: 15,
          type: "Лесной пожар",
          date: "2022-07-15",
        },
      ],
      test_polygon: [
        [37.290502, 55.8019897],
        [37.2932645, 55.7980647],
        [37.2931684, 55.7963971],
        [37.2941684, 55.7966347],
        [37.2941174, 55.7967126],
        [37.2944097, 55.7967872],
        [37.2944673, 55.7967167],
        [37.2982173, 55.7976281],
        [37.3023539, 55.7986335],
        [37.3027769, 55.8012728],
        [37.3029227, 55.8024772],
        [37.3032652, 55.8031819],
        [37.3035641, 55.8035588],
        [37.2996863, 55.8035219],
        [37.2986365, 55.8034501],
        [37.2977692, 55.803354],
        [37.2966321, 55.8032024],
        [37.2954221, 55.8029975],
        [37.290502, 55.8019897],
      ],
      geojson: null,
    };
  },

  // "https://nominatim.openstreetmap.org/search?q=Москва&format=json&polygon=1&polygon_geojson=1"
  mounted() {
    axios
      .get("https://nominatim.openstreetmap.org/search", {
        params: {
          q: "Москва",
          format: "json",
          polygon: 1,
          polygon_geojson: 1,
        },
      })
      .then((response) => {
        console.log(response.data);
        this.test_polygon = response.data[0].geojson.coordinates[0][0];

        // https://vue2-leaflet.netlify.app/components/LGeoJson.html#demo
        this.geojson = response.data[0].geojson;
        // console.log(this.test_polygon);
      })
      .catch((err) => {
        console.log(err);
      });
  },

  methods:{
    report(){
      //TODO
      // выбранная тема
      // список новостей
      // скрин карты
    },
  }
};
</script>
