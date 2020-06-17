<template>
  <div>
    <MapRender 
      :idList="idList" 
      :filteredMarker="filteredMarker" 
      :filteredBalloonMarker="filteredBalloonMarker"
      :balloonIdList="balloonIdList"
      @addStation="passStationFunc"
    />
  </div>
</template>

<script>
import L from 'leaflet';
import MapRender from './mapRender'

export default {
  props: ['stationList', 'message', 'messageRaw', 'balloonIds'],
  components: {
    MapRender
  },
  watch: {
    //  stations watchers (muri/stat)
    message(newVal) {
      this.payload = newVal
      this.filterMessage(this.payload)
    },
    stationList(newVal){
      this.idList = newVal
    },
    // balloon watchers (muri/raw)
    messageRaw(newVal) {
      this.payloadRaw = newVal
      this.filterMessageRaw(this.payloadRaw)
    },
    balloonIds(newVal) {
      this.balloonIdList = newVal
    },
    station(newVal) {
      this.$emit('as2', newVal)
    }
  },
  data() {
    return {
      payload: [],
      station: '',
      payloadRaw: [],
      filteredMarker: {},
      filteredBalloonMarker: {},
      idList: [],
      balloonIdList: []
    }
  },
  methods: {
    filterMessage(message){
      const messageOBJ = JSON.parse(message)
      if (this.idList !== [undefined]) {
        this.assignDataObjects(messageOBJ)
      }
    },
    filterMessageRaw(message){
      const messageOBJ = JSON.parse(message)
      if (this.balloonIdList !== [undefined]) {
        this.assignDataObjectsRaw(messageOBJ)
      }
    },
    assignDataObjects(message){
        const id = message['station']
        this.lat = message.tracker.gps['gps_lat'] 
        this.lon = message.tracker.gps['gps_lon']
        try {
          var marker = {
            [id] : L.latLng(this.lat, this.lon)
          }
        } catch {
          return
        }
        this.filteredMarker = marker
    },
    assignDataObjectsRaw(message){
        const id = message.data['ADDR_FROM']
        this.latLngDataCleanup(message.data.frame_data['gps_lat'], message.data.frame_data['gps_lon'])
        try {
          var marker = {
            [id] : L.latLng(this.latBalloon, this.lonBalloon)
          }
        } catch {
          return
        }
        this.filteredBalloonMarker = marker
    },
    latLngDataCleanup(latitude, longitude){
      const lat = (latitude  / 10000000).toFixed(2)
      const lon = (longitude / 10000000).toFixed(2)
      this.latBalloon = lat
      this.lonBalloon = lon
    },
    passStationFunc(station){
      this.station = station
    }
  }
}
</script>