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
        <cluster-table
          :items="clusters"
          :allDataLoaded="allDataLoaded"
          :loading="loading"
          @fetchData="loadClusters"
          @rowClick="rowClick"
        />
        <!--           @rowClick="rowClick" -->
        <!-- <v-data-table
          :headers="headers"
          :items="clusters"
          :items-per-page="20"
          fill-height
        >
        </v-data-table> -->
      </v-row>
    </v-col>

    <!-- карта -->
    <v-col cols="12" md="8" no-gutters class="pa-1">
      <l-map style="height: 100%" :zoom="zoom" :center="center">
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
import ClusterTable from "../components/ClusterTable.vue";
import http from "../http";

export default {
  name: "Case1View1",

  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LGeoJson,
    ClusterTable,
    // LMarker,
  },

  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [55.751244, 37.618423],

      loading: false,
      allDataLoaded: false,
      page: 1,
      clusters: [
        {
          theme: ["Лесной", "пожар", "Якутия"],
          articlesCount: 13,
          className: "Лесной пожар",
          dt: "2022-07-15",
          location:"Якутия",
        },
        {
          theme: ["Пожар", "Москва"],
          articlesCount: 2,
          className: "Пожар",
          dt: "2022-07-15",
          location:"Москва",
        },
        {
          theme: ["Нефтепровод", "Северный", "поток"],
          articlesCount: 20,
          className: "Авария",
          dt: "2022-11-20",
          location:"Остров Борнхольм",
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

  methods: {
    async getGeoJSON(name){
      await axios
      .get("https://nominatim.openstreetmap.org/search", {
        params: {
          q: name,
          format: "json",
          polygon: 1,
          polygon_geojson: 1,
        },
      })
      .then((response) => {
        // https://vue2-leaflet.netlify.app/components/LGeoJson.html#demo
        this.geojson = response.data[0].geojson;
        console.log(response.data[0]);
        this.center = [response.data[0].lat, response.data[0].lon];
        return response.data[0].geojson;
      })
      .catch((err) => {
        console.log(err);
        return null;
      });
    },

    async loadClusters() {
      this.loading = true;
      const response = await http.getList("Cluster", {
        showSnackbar: true,
        filters: {
          per_page: 20,
          page: this.page,
        },
      });
      this.clusters = [...this.clusters, ...response.data.items];
      this.page += 1;
      if (!response.data.items.length) this.allDataLoaded = true;
      this.loading = false;
    },
    rowClick(row) {
      // TODO запрос локации и отрисовка полигона
      console.log("rowClick(), row = ", row);
      var geojson = this.getGeoJSON(row.location);
      console.log("rowClick(), geojson = ", geojson);
    },

    report() {
      //TODO
      // выбранная тема
      // список новостей
      // скрин карты
    },
  },
};
</script>
