<template>
  <div>
    <MapRender :idList="idList" :filteredMarker="filteredMarker" />
  </div>
</template>

<script>
import L from 'leaflet';
import MapRender from './mapRenderMarkers'

export default {
  props: ['id', 'message'],
  components: {
    MapRender
  },
  watch: {
    message(newVal) {
      this.payload = newVal
      this.filterMessage(this.payload)
    },
    id(newVal){
      this.idList = newVal
    }
  },
  data() {
    return {
        payload: [],
        messageOBJ: [],
        idList: [],
        filteredMarker: {},
        rssi: Number
    }
  },
  methods: {
    filterMessage(message){
        this.messageOBJ = JSON.parse(message)
        if (this.idList !== undefined) {
          this.assignDataObjects(this.messageOBJ)
        }
    },
    assignDataObjects(message){
        const id = message.data['ADDR_FROM']
        this.latLngDataCleanup(message.data.frame_data['gps_lat'], message.data.frame_data['gps_lon'])
        this.filteredMarker = {
            [id] : L.latLng(this.lat, this.lon)
            }
        },
    latLngDataCleanup(latitude, longitude){
        const lat = (latitude / 10000000).toFixed(2)
        const lon = (longitude / 10000000).toFixed(2)
        this.lat = lat
        this.lon = lon
        }
    }
}
</script>