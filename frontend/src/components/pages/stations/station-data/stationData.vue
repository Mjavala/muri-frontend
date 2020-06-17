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
            :station="station"/>
          <div id="data-wrap">
            <div class="spacing">
              <balloonInfo id="balloon-info" :balloonToTrack="balloonToTrack" :balloonInfoMessage="balloonInfoMessage"/>
              <trackingInfo id="tracking-info" :stationTrackingInfoMessage="stationTrackingInfoMessage"/>
            </div>
            <div class="spacing">
              <div class="spacing-2">
                <mqttStats id="mqtt-stats" :stationTrackingInfoMessage="stationTrackingInfoMessage"/>
                <positionalInfo id="positional-info" :stationTrackingInfoMessage="stationTrackingInfoMessage" />
              </div>
            </div>
          </div>
        </v-content>
    </div>
</template>

<script>
import mqttReceiver from './mqttReceiver'
import NavBar from './navbarStation'
import Loader from '../../../loader'
import balloonInfo from '../../../info-cards/balloonInfo'
import positionalInfo from '../../../info-cards/positionalInfo'
import trackingInfo from '../../../info-cards/trackingInfo'
import mqttStats from '../../../info-cards/mqttStats'

export default {
  components: {
    mqttReceiver,
    NavBar,
    Loader,
    balloonInfo,
    trackingInfo,
    mqttStats,
    positionalInfo

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
      console.log(this.balloonToTrack)

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
  #balloon-info, #positional-info, #tracking-info, #mqtt-stats {
    display: inline;
  }
  #balloon-info{
    padding: 0.5em;
    padding-bottom: 0;
  }
  #mqtt-stats {
    margin-top: 5em;
    padding: 1em;
    padding-bottom: 0;

  }
  .spacing {
    padding: 0.25em;
    padding-bottom: 0;
  }
  .spacing-2 {
    display: inline;
    width: 20em;
    padding: 2.5em;
    padding-bottom: 0;
  }
</style>
