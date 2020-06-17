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
import {LMap, LTileLayer, LMarker, LIcon, LCircle} from 'vue2-leaflet'
import L from 'leaflet';
import Station from '../../../assets/broadcast.png'
import Balloon from '../../../assets/pin.png'

export default {
  components: { 
    LMap, 
    LTileLayer, 
    LMarker,
    LIcon,
    LCircle
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
    'filteredMarker', 'idList', 'filteredBalloonMarker', 'balloonIdList'
  ],
  watch: {
    filteredMarker(newVal){
      let objKey = Object.keys(newVal)
      this.currentDevice = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
      this.currentPosition = objKeyMap[0]
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
    updateBalloonMarker(i) {
      this.markersBalloon[i].latlng = L.latLng(this.currentBalloonPosition.lat, this.currentBalloonPosition.lng)
    },
    matchDeviceId () {
      for (const [i, markersObj] of this.markers.entries()) {
        if (this.currentDevice === markersObj.id) {
          this.updateMarker(i)
        }
      }
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
        latlng: L.latLng(this.currentPosition.lat, this.currentPosition.lng)
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

  @media only screen and (max-width: 768px) {
    .map{
      height: 50vh;
      width: 100vw;
      display: inherit;
      margin: 1% auto;
      margin-top: 15%;
      margin-bottom: 10%;
    }
  }
</style>