<template>
  <div>
      <filterMapData 
        :id='deviceList' 
        :message='payload' 
        :payloadStat='payloadStat'
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
  
  props: ['message', 'messageStat'],
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
    }
  },
  data() {
    return {
        payload: [],
        payloadStat: [],
        messageOBJ: [],
        deviceList: [],
        listOfIds: new Set(), //Set() -  list of unique items
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
