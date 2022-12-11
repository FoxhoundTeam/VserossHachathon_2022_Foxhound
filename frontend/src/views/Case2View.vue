<template>
  <v-row style="height: 100%" no-gutters fill-height>

    <!-- настройки -->
    <v-col cols="12" md="4" no-gutters class="pa-1">

      <!-- кнопка рассчитать и скачать файл -->
      <v-btn color="primary" @click="modeling" :loading="is_modeling">
        <v-icon v-if="!is_modeling">mdi-airplane-clock</v-icon>
        Провести моделирование
      </v-btn>

      <v-alert>
        
      </v-alert>

      <v-card flat class="fill-height d-flex flex-column ma-1">
        <v-card-text>
          <p class="font-weight-black">Кейс 2. Демонстрация динамической модели наведения дрона</p>
          <p class="font-weight-bold">Исходные данные:</p>
          <p class="font-italic">
            1) Полётное задание дрона в виде массива маршрутных точек;<br />
            2) Линия движения цели (на данный момент движение цели<br />
            задаётся прямой линией и цель движется равномерно);<br />
          </p>
          <p class="font-weight-bold">Описание:</p>
          <p class="font-italic">
            1) Реализована динамическая имитационная модель движения и наведения дрона;<br />
            2) Если цель во время полёта дрона не оказывается в его поле зрения, дрон отрабатывает
            полётное задание и возвращается в исходную точку;<br />
            3) Если движущаяся цель попадает в зону обзора дрона, дрон переходит на её сопровождение параллельным курсом.<br />
            4) Смоделированные параметры полёта дрона после окончания моделирования выгружаются в браузере в виде таблицы CSV
            и могут быть визуализированы с помощью отдельного модуля ().
          </p>
        </v-card-text>
      </v-card>

    </v-col>

    <!-- карта назначения полётного задания и движения цели -->
    <v-col cols="12" md="8" no-gutters class="pa-1">
      <l-map
        style="height: 100%;" :zoom="zoom" :center="center" ref="map">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <!-- <l-polygon :lat-lngs="test_polygon" :color="'green'"></l-polygon> -->

        <!-- https://vue2-leaflet.netlify.app/components/LGeoJson.html#demo -->
        <!-- <l-geo-json :geojson="geojson"></l-geo-json> -->
        <!--  -->
        <!-- <l-marker :lat-lng="markerLatLng"></l-marker> -->
      </l-map>
    </v-col>

  </v-row>
</template>

<script>
// @ is an alias to /src

// import axios from "axios";
import L from 'leaflet';
import {
  LMap,
  LTileLayer /*, LMarker */,
  // LControl,
  // LPolygon,
  // LGeoJson,
} from "vue2-leaflet";
// import LDraw from 'leaflet-draw'; // устаревший
import "leaflet/dist/leaflet.css";
import '@geoman-io/leaflet-geoman-free';  
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css';  

export default {
  name: 'Case2View',

  components: {
    LMap,
    LTileLayer,
    // LPolygon,
    // LGeoJson,
    // LMarker,
  },


  data() {
    return {
      // для карты
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [55.751244, 37.618423],
      mapobject : null,

      // прочие переменные страницы
      is_modeling : false,
    }
  },

  mounted(){
    this.mapobject = this.$refs.map.mapObject;
    /* для устаревшего leaflet-draw */
    // var map = L.map('map').setView([51.505, -0.09], 13);
    // L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    //   attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    // }).addTo(map);
    // 
    // this.mapobject.addControl(new L.Control.Fullscreen());

    // var map = this.$refs.map.mapObject;
    // console.log('mounted(), map = ', this.mapobject)
    // // FeatureGroup is to store editable layers
    // var drawnItems = new L.FeatureGroup();
    // this.mapobject.addLayer(drawnItems);
    // LDraw.Draw
    // var drawControl = new window.L.Control.Draw({
    //   position: 'topright',
    //   edit: {
    //     featureGroup: drawnItems
    //   }
    // });
    // console.log('mounted(), drawControl = ',drawControl);
    // this.mapobject.addControl(drawControl);

    L.marker([51.50915, -0.096112], { pmIgnore: true }).addTo(this.mapobject);
    // layer.options.pmIgnore = false;
    // L.PM.reInitLayer(layer);  
    this.mapobject.pm.setLang('ru');
    this.mapobject.pm.addControls({  
      position: 'topleft',  
      drawCircle: false, // отмена круговой области в панели
      drawMarker: false,// отмена маркера
      drawCircleMarker: false,// отмена кругового маркера
      drawText: false,// отмена текста
    });
  },

  methods: {
    modeling(){
      this.is_modeling = true;
      var layers = this.mapobject.pm.getGeomanLayers();
      var target_route = null;
      var drone_route = null;
      for (let layer_n = 0; layer_n < layers.length; layer_n++) {
        var layer = layers[layer_n];
        if(layer.toGeoJSON().geometry.type ==="LineString"
          && layer.toGeoJSON().geometry.coordinates.length === 2){
          target_route = layer.toGeoJSON().geometry.coordinates;
          console.log("target_route = ", target_route);
        }
        else if (layer.toGeoJSON().geometry.type ==="LineString"
          && layer.toGeoJSON().geometry.coordinates.length > 2)
        {
          drone_route = layer.toGeoJSON().geometry.coordinates;
          console.log("drone_route = ", drone_route);
        }
      }
      var result = {drone_route:drone_route, target_route:target_route};
      console.log("modeling(), result = ", JSON.stringify(result));

      // if
      //TODO уведомления
      //TODO ajax-запрос
    },
  },
}
</script>
