<template>
  <div id="app">
    <div id="wrapper">
      <v-btn icon depressed rounded id="live" v-if="this.status">
        <v-icon id="live-icon" color="#76FF03">mdi-wifi</v-icon>
      </v-btn>
      <filterID v-bind:message="this.message" />
      <div id='conFeedWrap'>
        <v-btn id="connect" @click="connect">
          Connect
        </v-btn>
        <v-btn id="disconnect" @click="disconnect">
          Disconnect
        </v-btn>
      </div>
    </div>
    <Feed v-bind:message="message" />
  </div>
</template>

<script>
import filterID from './filterID'
import Feed from './feed'

export default {
  props:
  ['station'],
  watch: {
    station(newVal) {
      this.stationFilter = newVal
    }
  },
  data () {
    return {
      message: '',
      logs: [],
      status: false,
      stationFilter: '',
      clientID: "clientID-" + parseInt(Math.random() * 100),
      host: 'irisslive.net',
      port: 9001,
      username: 'muri',
      password: 'demo2020'
    }
  },
  components: {
    filterID,
    Feed
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
        this.status = true
        this.client.subscribe("muri/raw");
        console.log('subscribed to muri/raw')
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
      this.status = false
    },
    disconnect(){
      this.client.disconnect()
      this.status = false
    },
    onMessageArrived(message) {
      const messageOBJ = JSON.parse(message.payloadString)
      if (messageOBJ['station'] === this.stationFilter){
        this.message = message.payloadString
      }
    },
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
  #conFeedWrap{
    margin-top: 3%;
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
  #disconnect {
    z-index: 11;
  }
  @media only screen and (max-width: 768px) {
    #connect {
      position: absolute;
      top: -4%;
      right: 52.5%;
    }
    #disconnect {
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