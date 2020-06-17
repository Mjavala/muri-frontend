<template>
    <div>
        <Loader v-if="show"></loader>
        <NavBar :station="station"/>
        <v-content>
          <mqttReceiver 
            @rawMessage="passSawMsg" 
            @statMessage="passStatMsg"
            :connectReq="connectReq" 
            :disconnectReq="disconnectReq" 
            :station="station"
          />
          <trackingInfo id="station-tracking-info" :stationTrackingInfoMessage="stationTrackingInfoMessage" />
          <div id="info-wrap">
            <positionalInfo id="positional-info-2" :stationTrackingInfoMessage="stationTrackingInfoMessage" />
            <mqttStats id="mqtt-stats-2" :stationTrackingInfoMessage="stationTrackingInfoMessage" />
          </div>
        </v-content>
    </div>
</template>

<script>
import mqttReceiver from './mqttReceiver'
import NavBar from './navbarStation'
import Loader from '../../../loader'
import trackingInfo from './info-cards/trackingInfo'
import positionalInfo from './info-cards/positionalInfo'
import mqttStats from './info-cards/mqttStats'

export default {
  components: {
    mqttReceiver,
    NavBar,
    Loader,
    trackingInfo,
    positionalInfo,
    mqttStats
  },
  data () {
    return {
      show: true,
      id: '',
      station: '',
      connectReq: false,
      disconnectReq: false,
      balloonInfoMessage: '',
      stationTrackingInfoMessage: '',
      balloonToTrack: ''
    }
  },
  watch: {
    id(newVal) {
      this.station = newVal
    }
  },
  created () {
    this.id = this.$route.params.id
  },
  mounted() {
    this.showToggle()
  },
  methods: {
    showToggle(){
      setTimeout(() => {
        this.show = false
      }, 1500)
    },
    passSawMsg (newVal) {
      this.balloonInfoMessage = newVal
    },
    passStatMsg (newVal) {
      this.stationTrackingInfoMessage = newVal
      this.getBalloonToTrack()

    },
    getBalloonToTrack() {
      const messageOBJ = JSON.parse(this.stationTrackingInfoMessage)
      const balloon = Object.keys(messageOBJ.current_tracks)
      // currently tracking first balloon in current_tracks
      this.balloonToTrack = balloon[0]
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
  #data-wrap {
    display: flex;
    margin-top: 1.5em;
  }
  #tracking-info {
      width: 100% !important;
  }
  #station-tracking-info {
    margin-top: 4em;
  }
  #balloon-info{
    padding: 0.5em;
    padding-bottom: 0;
  }
  #mqtt-stats-2{
    width: 40%;
  }
  .spacing {
    padding: 0.25em;
  }
  .spacing-2 {
      position: absolute;
      left: 0;
      width: 15em;
  }
  #info-wrap {
    display: flex;
  }
  #positional-info-2 {
    width: 50%;
  }
</style>
