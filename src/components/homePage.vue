<template>
    <div>
        <Loader v-if="show"></loader>
        <NavBar/>
        <v-content>
        <mqttReceiver />
        </v-content>
    </div>
</template>

<script>
import mqttReceiver from './mqttReceiver'
import NavBar from './navbar'
import Loader from './loader'

export default {

  components: {
    mqttReceiver,
    NavBar,
    Loader
  },
  data () {
    return {
      show: true
    }
  },
  mounted() {
    this.showToggle()
  },
  methods: {
    showToggle(){
      setTimeout(() => {
        this.show = false
      }, 1500)
    }
  }
};
</script>

<style scoped>
  #v-content{
    padding: 0px;
  }
  #app{
    margin: 0 !important;
  }
</style>
