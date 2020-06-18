<template>
  <div class="map">
    <l-map 
      v-bind="mapConfig"
    >
    <l-tile-layer 
      v-bind="mapRender"
    />
    <l-marker
        :key="marker.id"
        v-for="marker in markersBalloon"
        :lat-lng="marker.latlng"
      >
      <l-icon v-bind="iconConfigBalloon" />
    </l-marker>
      <l-polyline
        :key="marker.id + 'line'"
        v-for="marker in markers"
        :lat-lngs="marker.polylines"
        :opacity="1"
        :weight="3"
      >
      </l-polyline>
    <l-marker
        :key="marker.id"
        v-for="marker in markers"
        :lat-lng="marker.latlng"
        :options="{alt: marker.id}"
      >
      <l-icon v-bind="iconConfig" />
    </l-marker>
    <l-circle
      :key="'circle' + marker.id"
      v-for="marker in markers"
      :lat-lng="marker.latlng"
      :radius="185200"
      :opacity="0.75"
      :fillOpacity="0.1"
    >
    </l-circle>
    </l-map>
  </div>
</template>

<script>
//TODO: Test render of markers / popups / prop data
import {LMap, LTileLayer, LMarker, LIcon, LCircle, LPolyline} from 'vue2-leaflet'
import L from 'leaflet';
import Station from '../../../assets/broadcast.png'
import Balloon from '../../../assets/pin.png'

export default {
  components: { 
    LMap, 
    LTileLayer, 
    LMarker,
    LIcon,
    LCircle,
    LPolyline,
  },
  mounted () {
    document.addEventListener('click', (e) => {
      for (const [i, markersObj] of this.markers.entries()) {
        if (e.target.alt === markersObj.id) {
          this.$emit('addStation', this.markers[i].id)
        }
      }
    })
  },
  props: [
    'filteredMarker', 'idList', 'filteredBalloonMarker', 'balloonIdList', 'filteredAzimuth', 'filteredElevation'
  ],
  watch: {
    filteredMarker(newVal){
      let objKey = Object.keys(newVal)
      this.currentDevice = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
      this.currentPosition = objKeyMap[0]
    },
    filteredAzimuth (newVal) {
      let objKey = Object.keys(newVal)
      this.currentDeviceAzimuth = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
      this.currentAzimuth = objKeyMap[0]
      this.matchDeviceIdForPolyline()
    },
    filteredElevation (newVal) {
      let objKey = Object.keys(newVal)
      this.currentDeviceElevation = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
      this.currentElevation = objKeyMap[0]
      this.matchDeviceIdForElevation()
    },
    idList(newVal, oldVal){
      if (newVal.length === oldVal.length){
        // loop through array and find the array index that matches the 'currentDevice'
        // update the 'markers' array L.latlng field at the given index
        this.matchDeviceId()
      }
      if (newVal.length > oldVal.length && newVal.length > 1){
        // new device detected, push the 'filteredMarkers' object into the 'markers' array
        this.addMarkerToMarkerArray()
      }
      if (newVal.length === 1){
        // first device, add the first marker
        if (this.count === 0){
          this.addMarkerToMarkerArray()
          this.count = this.count + 1
        }
      }
    },
    filteredBalloonMarker(newVal) {
      let objKey = Object.keys(newVal)
      this.currentBalloon = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k])
      this.currentBalloonPosition = objKeyMap[0]
    },
    balloonIdList(newVal, oldVal) {
      if (newVal.length === oldVal.length){
        // loop through array and find the array index that matches the 'currentDevice'
        // update the 'markers' array L.latlng field at the given index
        this.matchBalloonId()
      }
      if (newVal.length > oldVal.length && newVal.length > 1){
        // new device detected, push the 'filteredMarkers' object into the 'markers' array
        this.addMarkerToBalloonMarkerArray()
      }
      if (newVal.length === 1){
        // first device, add the first marker
        if (this.countBalloon === 0){
          if ('lat' in this.currentBalloonPosition) {
            this.addMarkerToBalloonMarkerArray()
            this.countBalloon = this.countBalloon + 1
          }
        }
      }
    }
  },
  data() {
    return {
      markers: [],
      markersBalloon: [],
      currentDevice: '',
      currentAzimuth: Number,
      currentElevation: Number,
      bearing: Number,
      currentDeviceAzimuth: '',
      currentDeviceElevation: '',
      currentBalloon: '',
      currentPosition: {},
      currentBalloonPosition: {},
      count: 0,
      countBalloon: 0,
      mapConfig: {
        zoom: 7,
        minZoom: 2,
        center: L.latLng(40, -105),
        Bounds: [
          [-90, -180],
          [90, 180]
        ],
        maxBounds: [
          [-90, -180],
          [90, 180]
        ],
      },
      iconConfig: {
        'icon-url': Station,
        'icon-size': [30,30],
      },
      iconConfigBalloon: {
        'icon-url': Balloon,
        'icon-size': [30,30],
      },
      mapRender: {
        url:'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
      },
    }
  },
  methods: {
    latLng(lat,long){
      return L.latLng(lat,long)
    },
    updateMarker(i) {
      this.markers[i].latlng = L.latLng(this.currentPosition.lat, this.currentPosition.lng)
    },
    updateElevation(i) {
      this.markers[i].elevation = this.currentElevation
    },
    updateBalloonMarker(i) {
      this.markersBalloon[i].latlng = L.latLng(this.currentBalloonPosition.lat, this.currentBalloonPosition.lng)
    },
    matchDeviceId () {
      for (const [i, markersObj] of this.markers.entries()) {
        if (this.currentDeviceAzimuth === markersObj.id) {
          this.updateMarker(i)
        }
      }
    },
    matchDeviceIdForPolyline () {
      for (const [i, markersObj] of this.markers.entries()) {
        if (this.currentDeviceAzimuth === markersObj.id) {
          this.pushPolylineArray(i)
        }
      }
    },
    matchDeviceIdForElevation () {
      for (const [i, markersObj] of this.markers.entries()) {
        if (this.currentDeviceElevation === markersObj.id) {
          this.updateElevation(i)
        }
      }
    },
    pushPolylineArray (i) {
      const start = L.latLng(this.currentPosition.lat, this.currentPosition.lng)
      const end = this.calculatePolylineEndpoint(this.currentPosition, this.currentAzimuth)
      this.markers[i].polylines = [start, end]
    },
    calculatePolylineEndpoint(start, azimuth) {
      if (azimuth >= 0 && azimuth <= 90) {
        this.bearing = azimuth
      }
      if (azimuth >= 90 && azimuth <= 180) {
        this.bearing = 180 - azimuth
      }
      if (azimuth >= 180 && azimuth <= 270) {
        this.bearing = azimuth - 180
      }
      if (azimuth >= 270 && azimuth <= 360) {
        this.bearing = 360 - azimuth
      }
        const R = 6378.1
        const brng = this.bearing * Math.PI / 180
        const d = 185.2 
        const lat1 = start.lat *  Math.PI / 180
        const lon1 = start.lng *  Math.PI / 180
        const lat2 = Math.asin( Math.sin(lat1) * Math.cos(d/R) + Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng))
        const lon2 = lon1 + Math.atan2(Math.sin(brng)*Math.sin(d/R)*Math.cos(lat1), Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2))

        const lat2Final = lat2 * 180 / Math.PI
        const lon2Final = lon2 * 180 / Math.PI
        const endpoint = L.latLng(lat2Final, lon2Final)
        return endpoint
    },
    matchBalloonId () {
      for (const [i, markersObj] of this.markersBalloon.entries()) {
        if (this.currentBalloon === markersObj.id) {
          this.updateBalloonMarker(i)
        }
      }
    },
    addMarkerToMarkerArray() {
      const markerObj = {
        id: this.currentDevice,
        latlng: L.latLng(this.currentPosition.lat, this.currentPosition.lng),
        polylines: [],
        elevation: Number
      }
      this.markers.push(markerObj)
    },
    addMarkerToBalloonMarkerArray() {
      const markerObj = {
        id: this.currentBalloon,
        latlng: L.latLng(this.currentBalloonPosition.lat, this.currentBalloonPosition.lng)
      }
      this.markersBalloon.push(markerObj)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.map{
  height: 85vh;
  width: 75vw;
  display: inherit;
  padding: 2% 2% 0 1%;
  margin-top: 3.5%;
}
.leaflet-container a.leaflet-popup-close-button{
  color: #121212;
  width: 15px;
  padding: 0;
}
.leaflet-popup-content-wrapper, .leaflet-popup-tip{
  background: #121212;
}
.leaflet-control-attribution {
  display: none;
}
.leaflet-marker-icon{
  opacity: .85;
}
.leaflet-control-zoom {
  padding: 2%;
  border: none !important;
}
.leaflet-control-zoom-in{
  background: white !important;
  color: #121212 !important;
}
.leaflet-control-zoom-out{
  background: white !important;
  color: #121212 !important;
}
</style>