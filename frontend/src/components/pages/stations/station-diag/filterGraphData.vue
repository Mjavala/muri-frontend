<template>
  <div>
    <rssiGraph :idList="idList" :filteredRSSI="filteredRSSI" />
    <voltageGraph :idList="idList" :filteredVoltage="filteredVoltage" />
    <currentGraph :filteredAzimuth="filteredAzimuth" :filteredElevation="filteredElevation" />

  </div>
</template>

<script>
import rssiGraph from './graphs/rssiGraph'
import currentGraph from './graphs/currentGraph'
import voltageGraph from './graphs/voltageGraph'

export default {

  props: ['id', 'message', 'payloadStat'],
  components: {
    rssiGraph,
    voltageGraph,
    currentGraph
  },
  watch: {
    message(newVal) {
      this.payload = newVal
      this.filterMessage(this.payload)
    },
    id(newVal){
      this.idList = newVal
    },
    payloadStat (newVal) {
      this.payloadStats = newVal
      this.filterMessageStat(this.payloadStats)
    }
  },
  data() {
    return {
        payload: [],
        payloadStats: [],
        messageOBJ: [],
        idList: [],
        filteredVoltage: {},
        filteredAzimuth: {},
        filteredElevation: {},
        filteredRSSI: {},
        rssi: Number,
        time: new Date()
    }
  },
  methods: {
    filterMessage(message){
      this.messageOBJ = JSON.parse(message)
      this.assignDataObjects(this.messageOBJ)
    },
    filterMessageStat(message){
      this.messageOBJ = JSON.parse(message)
      this.assignDataObjectsStation(this.messageOBJ)
    },
    assignDataObjects(message){
      const id = message.data['ADDR_FROM']
      
      this.filteredRSSI = {
          [id] : message.data['RSSI_RX']
        }
      },
    assignDataObjectsStation (message) {
      const id = message['station']

      this.filteredVoltage = {
        [id]: message.tracker.ant['volts']
        }
      this.filteredAzimuth = {
        [id]: message.tracker.ant['azm']
        }
      this.filteredElevation = {
        [id]: message.tracker.ant['elv']
        }
      }
    }
}
</script>