<template>
  <div>
    <altitudeGraph :idList="idList" :filteredAltitude="filteredAltitude" />
    <rssiGraph :idList="idList" :filteredRSSI="filteredRSSI" />
    <tempGraph :idList="idList" :filteredTemp="filteredTemp" />
    <humGraph :idList="idList" :filteredHum="filteredHum" />
  </div>
</template>

<script>
import altitudeGraph from './altitudeGraph'
import rssiGraph from './RSSIGraph'
import tempGraph from './temperatureGraph'
import humGraph from './humidityGraph'

export default {

  props: ['id', 'message'],
  components: {
    altitudeGraph,
    rssiGraph,
    tempGraph,
    humGraph
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
        filteredAltitude: {},
        filteredRSSI: {},
        filteredTemp: {},
        filteredHum: {},
        altitude: {},
        rssi: Number
    }
  },
  methods: {
    filterMessage(message){
        this.messageOBJ = JSON.parse(message)
        this.assignDataObjects(this.messageOBJ)
    },
    assignDataObjects(message){
        const id = message.data['ADDR_FROM']

        this.filteredAltitude = {
            [id] : message.data.frame_data['gps_alt']
          }
        this.filteredRSSI = {
            [id] : message.data['RSSI_RX']
          }
        this.filteredTemp = {
            [id]: message.data.frame_data['temp Ta1 (amb)']
          }
        //  need RS41 for humidity
        this.filteredHum = {
            [id]: message.data.frame_data['RS41 Hum']
          }
        }
    }
}
</script>