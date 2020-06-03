<template>
  <div>
    <altitudeGraph :idList="idList" :filteredAltitude="filteredAltitude" />
    <rssiGraph :idList="idList" :filteredRSSI="filteredRSSI" />
  </div>
</template>

<script>
import altitudeGraph from './altitudeGraph'
import rssiGraph from './RSSIGraph'

export default {

  props: ['id', 'message'],
  components: {
    altitudeGraph,
    rssiGraph
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
        }
    }
}
</script>