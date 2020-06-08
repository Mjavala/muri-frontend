<template>
  <div id="app">
    <div id="wrapper">
      <filterID :message='message'/>
      <div id='conndisc'>
        <v-btn id="connect-home" @click="connect">
          Connect
        </v-btn>
        <v-btn id="disconnect-home" @click="disconnect">
          Disconnect
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import filterID from './filterID'

export default{
  components: {
    filterID
  },
  data () {
    return {
      message: '',
      logs: [],
      live: false,
      clientID: "clientID-" + parseInt(Math.random() * 100),
      host: 'irisslive.net',
      port: 9001,
      username: 'muri',
      password: 'demo2020',
      stationList: new Set(),
      stations: []
    }
  },
  watch: {
    stations(newVal, oldVal){
      if (newVal.length === 1){
        this.$emit('stations', this.stations)
      }
      if (newVal.length > oldVal.length && newVal.length > 1){
        this.$emit('stations', this.stations)
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
        console.log("Connected");
        this.live = true
        this.client.subscribe("muri/stat");
        console.log('subscribed to muri/stat')

        this.$emit('live', this.live)
    },
    onConnectionLost(responseObject) {
      console.log('disconnected')
      if (responseObject.errorCode !== 0) {
        console.log(responseObject.errorCode)
        console.log("onConnectionLost:"+responseObject.errorMessage)
        this.client.connect({      
          onSuccess: this.onConnect,
          useSSL: true, 
          userName : this.username,
          password : this.password
          }
        )
        console.log('reconnecting')
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
      this.message = message.payloadString
      this.decodeMessageAndPassToParent(this.message)
    },
    decodeMessageAndPassToParent(message) {
      const messageOBJ = JSON.parse(message)
      this.stationList.add(messageOBJ['station'])
      this.stations = Array.from(this.stationList)
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
  @media only screen and (max-width: 768px) {
    #connect-home {
      position: absolute;
      top: -4%;
      right: 52.5%;
    }
    #disconnect-home {
      position: absolute;
      top: -4%;
      left: 50%;
    }
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