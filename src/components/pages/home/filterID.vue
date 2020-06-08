<template>
  <div>
      <filterMapData :id='deviceList' :message='payload' />
  </div>

</template>

<script>
import filterMapData from './filterMapData'

export default {
  
  props: ['message'],
  components: {
    filterMapData,
  },
  watch: {
    message(newVal) {
      this.payload = newVal
      this.addIdAndFilterMessage(newVal)
    }
  },
  data() {
    return {
        payload: [],
        messageOBJ: [],
        deviceList: [],
        listOfIds: new Set(), //Set() -  list of unique items
    }
  },
  methods: {
    addIdAndFilterMessage(message){
        this.messageOBJ = JSON.parse(message)
        this.listOfIds.add(this.messageOBJ['station'])
        this.deviceList = Array.from(this.listOfIds)
        }
    }
}
</script>
