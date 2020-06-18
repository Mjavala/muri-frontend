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
      <l-popup> 
        <div class="popups">
          alt(m): {{marker.altitude}}
        </div> 
      </l-popup>
      <l-icon v-bind="iconConfig" />
      </l-marker>
      <l-polyline
        :key="marker.id + 'line'"
        v-for="marker in markers"
        :lat-lngs="marker.pathLine"
        :color="'#76FF03'"
        :opacity="1"
        :weight="3"
        :dashArray="'12'"
      />
    </l-map>
  </div>
</template>

<script>
//TODO: Test render of markers / popups / prop data
import {LMap, LTileLayer, LMarker, LIcon, LPolyline , LPopup} from 'vue2-leaflet'
import L from 'leaflet';
import Pin from '../../../../assets/pin.png'

export default {
  components: { 
    LMap, 
    LTileLayer, 
    LMarker,
    LIcon,
    LPolyline,
    LPopup
  },
  props: [
    'filteredMarker', 'idList', 'filteredAltitude', 'balloonToTrack4'
  ],
  watch: {
    filteredMarker(newVal){
      let objKey = Object.keys(newVal)
      this.currentDevice = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k])
      this.currentPosition = objKeyMap[0]
      if (this.currentDevice === this.balloonToTrackFinal){
        this.mapConfig.center = L.latLng(this.currentPosition.lat, this.currentPosition.lng)
      }
    },
    filteredAltitude(newVal) {
      this.currentAltitude = (newVal).toFixed(1)
    },
    balloonToTrack4(newVal){
      this.balloonToTrackFinal = newVal
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
      currentAltitude: Number,
      currentPosition: {},
      balloonToTrackFinal: '',
      count: 0,
      mapConfig: {
        zoom: 13,
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
      this.markers[i].pathLine.push([this.currentPosition.lat, this.currentPosition.lng])
      this.markers[i].altitude = this.currentAltitude
    },
    matchDeviceId () {
      for (const [i, markersObj] of this.markers.entries()) {
        if (this.currentDevice === markersObj.id) {
          this.updateMarker(i)
        }
      }
    },
    addMarkerToMarkerArray () {
      const markerObj = {
        id: this.currentDevice,
        latlng: L.latLng(this.currentPosition.lat, this.currentPosition.lng),
        pathLine: [[this.currentPosition.lat, this.currentPosition.lng]],
        altitude: this.currentAltitude
      }
      this.markers.push(markerObj)
    }
  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.map{
  height: 60vh;
  width: 40vw;
  display: inherit;
  padding: 2% 2% 0 1%;
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