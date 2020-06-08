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
        v-for="marker in markers"
        :lat-lng="marker.latlng"
      >
        <l-icon v-bind="iconConfig" />
      </l-marker>
    </l-map>
  </div>
</template>

<script>
//TODO: Test render of markers / popups / prop data
import {LMap, LTileLayer, LMarker, LIcon} from 'vue2-leaflet'
import L from 'leaflet';
import Pin from '../../../../assets/pin.png'

export default {
  components: { 
    LMap, 
    LTileLayer, 
    LMarker,
    LIcon,
  },
  props: [
    'filteredMarker', 'idList'
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
        // update the 'markers' array L.latlng field at the given index ..
        this.matchDeviceId()
      }
      if (newVal.length > oldVal.length && newVal.length > 1){
        // new device detected, push the 'filteredMarkers' object into the 'markers' array
        this.addMarkerToMarkerArray()
      }
      if (newVal.length === 1){
        // first device, add the first marker
        if (this.count === 0){
          if (this.currentPosition !== undefined) {
            this.addMarkerToMarkerArray()
            this.count = this.count + 1
          }
        }
      }
    }
  },
  data() {
    return {
      markers: [],
      currentDevice: '',
      currentPosition: {},
      count: 0,
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
        'icon-url': Pin,
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
    matchDeviceId () {
      for (const [i, markersObj] of this.markers.entries()) {
        if (this.currentDevice === markersObj.id) {
          this.updateMarker(i)
        }
      }
    },
    addMarkerToMarkerArray() {
      const markerObj = {
        id: this.currentDevice,
        latlng: L.latLng(this.currentPosition.lat, this.currentPosition.lng)
      }
      this.markers.push(markerObj)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.map{
  height: 70vh;
  width: 50vw;
  display: inherit;
  padding: 2% 2% 2% 1%;
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