<template>
  <div id="map-graph-wrap">
      <filterMapData 
        :id='deviceList' 
        :message='payload' 
        :balloonToTrack3="balloonToTrack3"
      />
      <filterGraphData 
        :id='deviceList' 
        :message='payload' 
        :payloadStat='payloadStat'
      />
  </div>

</template>

<script>
import filterMapData from './filterMapData'
import filterGraphData from './filterGraphData'

export default {
  
  props: ['message', 'messageStat', 'balloonToTrack2'],
  components: {
    filterMapData,
    filterGraphData
  },
  watch: {
    message(newVal) {
      this.payload = newVal
      this.addIdAndFilterMessage(newVal)
    },
    messageStat(newVal) {
      this.payloadStat = newVal
    },
    balloonToTrack2(newVal) {
      this.balloonToTrack3 = newVal
    }
  },
  data() {
    return {
        payload: [],
        payloadStat: [],
        messageOBJ: [],
        deviceList: [],
        listOfIds: new Set(), //Set() -  list of unique items
        balloonToTrack3: '',
    }
  },
  methods: {
    addIdAndFilterMessage(message){
        this.messageOBJ = JSON.parse(message)
        this.listOfIds.add(this.messageOBJ.data['ADDR_FROM'])
        this.deviceList = Array.from(this.listOfIds)
      }
    }
  }
</script>

<style>
  #map-graph-wrap{
    position: relative;
    height: 60vh;
  }
</style>
