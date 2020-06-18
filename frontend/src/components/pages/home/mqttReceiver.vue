<template>
  <div id="app">
    <div id="wrapper">
      <filterID 
        :message='message' 
        :messageRaw="messageRaw"
        @addStation="passStationFunc"
      />
      <v-btn id="disconnect" @click="disconnect">
        Disconnect
      </v-btn>
    </div>
  </div>
</template>

<script>
import filterID from './filterID'

export default {
  components: {
    filterID
  },
  data () {
    return {
      message: '',
      messageRaw: '',
      logs: [],
      live: false,
      clientID: "clientID-" + parseInt(Math.random() * 100),
      host: 'irisslive.net',
      port: 9001,
      username: 'muri',
      password: 'demo2020',
      stationList: new Set(),
      stations: [],
      t0: Number,
      delta: 900000, // 1 min for test
      stationTimeObj: {},
      listOfStationTimeObj: [],
      count: 0,
      currentStation: ''
    }
  },
  mounted () {
    try {
      this.connect()
    } catch {
      console.log('!---Connect function failed ---!')
    }
    this.t0 = new Date()
  },
  watch: {
    stations(newVal, oldVal){
      this.t1 = new Date()
      if (newVal.length === oldVal.length){
        this.findTrace()
      }
      if (newVal.length > oldVal.length && newVal.length > 1){
        this.$emit('stations', this.stations)
        this.listOfStationTimeObj.push(this.stationTimeObj)
        this.findTrace()
      }
      if (newVal.length === 1){
        this.$emit('stations', this.stations)
        if (this.count === 0) {
          this.listOfStationTimeObj.push(this.stationTimeObj)
          this.count = this.count + 1
        }
      }
      // 900000 ms ~ 15 minutes
      if ((this.t1 - this.t0) > this.delta) {
        this.t0 = new Date()
        this.checkStationMessageTimestamp()
      }
    }
  },
  methods: {
    connect () {
      this.client = new window.Paho.MQTT.Client(this.host, this.port, this.clientID);
      this.client.connect({      
        onSuccess: this.onConnect,
        useSSL: true, 
        userName : this.username,
        password : this.password
        }
      );
      this.client.onMessageArrived = this.onMessageArrived;
      this.client.onConnectionLost = this.onConnectionLost
      this.client.onConnect = this.onConnect
    },
    onConnect(){
        // Once a connection has been made, make a subscription and send a message.
        console.log("Connected")
        this.live = true
        this.client.subscribe("muri/stat")
        this.client.subscribe("muri/raw")
        console.log('subscribed to muri/stat')
        console.log('subscribed to muri/raw')

        this.$emit('live', this.live)
    },
    onConnectionLost(responseObject) {
      console.log('disconnected')
      if (responseObject.errorCode !== 0) {
        console.log(responseObject.errorCode)
        console.log("onConnectionLost:"+responseObject.errorMessage)
        this.clientID = "clientID-" + parseInt(Math.random() * 100)
        this.client = new window.Paho.MQTT.Client(this.host, this.port, this.clientID)
        setTimeout(() => {
          this.client.connect({      
          onSuccess: this.onConnect,
          useSSL: true, 
          userName : this.username,
          password : this.password
          })
        console.log('reconnecting')
        }, 1000)
      }
      this.live = false
      this.$emit('live', this.live)
    },
    disconnect(){
      this.client.disconnect()
      this.status = false
      this.$emit('live', this.live)
    },
    onMessageArrived(message) {
      if (message.destinationName === 'muri/stat') {
        this.message = message.payloadString
        this.decodeMessageAndPassToParent(this.message)
      }
      if (message.destinationName === 'muri/raw'){
        const check = this.checkMessagePurity(message.payloadString)
        if (check === false) {
          return
        }
        if (check === true) {
          this.messageRaw = message.payloadString
        }
      }
    },
    decodeMessageAndPassToParent(message) {
      const messageOBJ = JSON.parse(message)
      this.stationList.add(messageOBJ['station'])
      this.currentStation = messageOBJ['station']
      this.stations = Array.from(this.stationList)
      this.stationTimeObj = {
        [messageOBJ['station']]: new Date()
      }
    },
    checkMessagePurity(message) {
      const messageOBJ = JSON.parse(message)
      if (messageOBJ.data.frame_data === undefined){
        return false
      } else {
        return true
      }
    },
    findTrace () {
      for (const [i, id] of this.listOfStationTimeObj.entries()){
        if (id === this.currentStation){
          this.addData(i)
        }
      }
    },
    addData (i) {
      this.listOfStationTimeObj[i] = new Date()
    },
    checkStationMessageTimestamp() {
      this.listOfStationTimeObj.forEach(element => {
        var station = Object.keys(element)[0]
        const key1 = Object.keys(element).map((k) => element[k])
        const timeDelta = this.t0 - Date.parse(key1)
        if (timeDelta > this.delta) {
          this.stations.forEach((element, i) => {
            if (element === station){
                this.stations.splice(i, 1)
            }
          })
        }
      })
    },
    passStationFunc (station) {
      this.$emit('stationsFromMap', station)
    }
  }
}
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 20px;
    position: relative;
  }
  #wrapper{
    position: relative;
    height: 105%;
  }
  #conndisc{
    margin-top: 1%;
  }
  #live{
    position: fixed;
    top: 1.5%;
    left: 18em;
    z-index: 1001;
    background: transparent;
  }
  #live-icon{
    animation: shadow-pulse 3s infinite;
    border-radius: 50%;
  }
  #disconnect-home {
    z-index: 11;
  }
  @keyframes shadow-pulse
  {
    0% {
      box-shadow: 0 0 0 0px rgba(0, 0, 0, 0.2);
    }
    100% {
      box-shadow: 0 0 0 15px rgba(0, 0, 0, 0);
    }
  }
</style>