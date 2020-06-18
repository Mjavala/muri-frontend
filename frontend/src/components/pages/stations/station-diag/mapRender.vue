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
          alt: {{marker.altitude}}
        </div> 
      </l-popup>
      <l-icon v-bind="iconConfigBalloon" />
      </l-marker>
      <l-marker v-if="this.statCount === 1" :lat-lng="statMarker">
        <l-icon v-bind="iconConfig" />
      </l-marker>
      <l-circle
        v-if="this.statCount === 1"
        :lat-lng="statMarker"
        :radius="185200"
        :opacity="0.75"
        :fillOpacity="0.1"
      >
      </l-circle>
      <l-polyline
        :key="marker.id + 'line'"
        v-for="marker in markers"
        :lat-lngs="marker.pathLine"
        :opacity="1"
        :weight="1"
        :dashArray="'12'"
      />
      <l-polyline
        v-if="this.statCount === 1"
        :lat-lngs="azimuthLine"
        :opacity="1"
        :weight="3"
      >
      <l-popup v-if="this.statCount === 1"> 
        <div class="popups">
          elv: {{this.elv}}
        </div> 
      </l-popup>
      </l-polyline>
    </l-map>
  </div>
</template>

<script>
//TODO: Test render of markers / popups / prop data
import {LMap, LTileLayer, LMarker, LIcon, LPolyline , LPopup, LCircle} from 'vue2-leaflet'
import L from 'leaflet';
import Pin from '../../../../assets/pin.png'
import Station from '../../../../assets/broadcast.png'


export default {
  components: { 
    LMap, 
    LTileLayer, 
    LMarker,
    LIcon,
    LPolyline,
    LPopup,
    LCircle
  },
  props: [
    'filteredMarker', 'idList', 'filteredAltitude', 'filteredMarkerStat', 'filteredAzimuth', 'filteredElevation'
  ],
  watch: {
    filteredMarker(newVal){
      let objKey = Object.keys(newVal)
      this.currentDevice = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
      this.currentPosition = objKeyMap[0]
    },
    filteredAltitude(newVal) {
      this.currentAltitude = (newVal).toFixed(1)
    },
    filteredMarkerStat(newVal) {
      let objKey = Object.keys(newVal)
      this.currentStation = objKey[0]
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k])
      this.currentStationPosition = objKeyMap[0]
      this.mapConfig.center = L.latLng(this.currentStationPosition.lat, this.currentStationPosition.lng)
      this.statMarker = objKeyMap[0]
      if(this.statCount === 0) {
        this.statCount = this.statCount + 1
      }
    },
    filteredAzimuth (newVal) {
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k])
      this.az = objKeyMap[0]
      if (this.az >= 0 && this.az <= 90) {
        this.bearing = this.az
      }
      if (this.az >= 90 && this.az <= 180) {
        this.bearing = 180 - this.az
      }
      if (this.az >= 180 && this.az <= 270) {
        this.bearing = this.az - 180
      }
      if (this.az >= 270 && this.az <= 360) {
        this.bearing = 360 - this.az
      }
      if(this.statCount === 1){
        const start = this.mapConfig.center
        const R = 6378.1
        const brng = this.bearing * Math.PI / 180
        const d = 185.2 
        const lat1 = start.lat *  Math.PI / 180
        const lon1 = start.lng *  Math.PI / 180
        const lat2 = Math.asin( Math.sin(lat1) * Math.cos(d/R) + Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng))
        const lon2 = lon1 + Math.atan2(Math.sin(brng)*Math.sin(d/R)*Math.cos(lat1), Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2))

        const lat2Final = lat2 * 180 / Math.PI
        const lon2Final = lon2 * 180 / Math.PI
        this.azimuthLineEnd = L.latLng(lat2Final, lon2Final)
        this.azimuthLine = [this.mapConfig.center, this.azimuthLineEnd]
      }
    },
    filteredElevation (newVal) {
      let objKeyMap = Object.keys(newVal).map((k) => newVal[k])
      this.elv = objKeyMap[0]
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
      azimuthLine: {},
      azimuthLineEnd: {},
      az: Number,
      elv: Number,
      bearing: Number,
      statMarker: {},
      statCount: 0,
      currentDevice: '',
      currentAltitude: Number,
      currentPosition: {},
      currentStation: '',
      currentStationPosition: {},
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
      iconConfigBalloon: {
        'icon-url': Pin,
        'icon-size': [30,30],
      },
      iconConfig: {
        'icon-url': Station,
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
  width: 50vw;
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