<template>
  <div>
      <filterMapData 
        :stationList='stationList' 
        :message='payload' 
        :messageRaw="payloadRaw" 
        :balloonIds="balloonIds"
        @as2="yo"
      />
  </div>

</template>

<script>
import filterMapData from './filterMapData'

export default {
  
  props: ['message', 'messageRaw'],
  components: {
    filterMapData,
  },
  watch: {
    message(newVal) {
      this.payload = newVal
      this.addIdAndFilterMessage(newVal)
    },
    messageRaw(newVal) {
      this.payloadRaw = newVal
      this.addIdAndFilterMessageRaw(newVal)
    }
  },
  data() {
    return {
        payload: [],
        payloadRaw: [],
        messageOBJ: [],
        messageOBJRaw: [],
        stationList: [],
        balloonIds: [],
        uniqueStations: new Set(), //Set() -  list of unique items (station)
        uniqueBalloons: new Set()
    }
  },
  methods: {
    addIdAndFilterMessage(message){
      this.messageOBJ = JSON.parse(message)
      this.uniqueStations.add(this.messageOBJ['station'])
      this.stationList = Array.from(this.uniqueStations)
    },
    addIdAndFilterMessageRaw(message){
      this.messageOBJRaw = JSON.parse(message)
      this.uniqueBalloons.add(this.messageOBJRaw.data['ADDR_FROM'])
      this.balloonIds = Array.from(this.uniqueBalloons)
    },
    yo (station) {
      console.log(station)
      this.$emit('addStation', station)
    }
  }
}
</script>
