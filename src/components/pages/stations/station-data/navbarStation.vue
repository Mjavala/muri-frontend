<template>    
    <v-app-bar
        app
        dark
        id="nav"
    >
      <v-img id="iriss-logo" max-height="100" max-width="225" src="../../../../assets/iriss_logo.png" />
      <v-spacer />
      <v-btn light small>
          <router-link to="/">Home</router-link>
      </v-btn>
    
      <v-btn small light class="graph-button active" id="alt" @click="graphButtonsActive">
        Alt
      </v-btn>
      <v-btn small light class="graph-button active" id="rssi" @click="graphButtonsActive">
        Rssi
      </v-btn>
      <v-btn small light class="graph-button" id="temp" @click="graphButtonsActive">
        Temp
      </v-btn>
      <v-btn small light class="graph-button" id="hum" @click="graphButtonsActive">
        Hum
      </v-btn>
    </v-app-bar>
</template>

<script>
export default {
  methods: {
    graphButtonsActive (event) {
      const targetButton = event.target.getAttribute('id')
      const targetClassParent = event.target.parentNode.getAttribute('id')
      if (targetButton !== null) {
        event.target.classList.add('active')
        if (targetButton === 'temp') {
          const altGraph = document.getElementById('altitude-graph')
          const alt = document.getElementById('alt')
          alt.classList.remove('active')
          // graph no show
          altGraph.classList.add('noShowGraph')
        }
        if (targetButton === 'hum') {
          const rssiGraph = document.getElementById('rssi-graph')
          const rssi = document.getElementById('rssi')
          rssi.classList.remove('active')
          // graph no show
          rssiGraph.classList.add('noShowGraph')
        }
        if (targetButton === 'alt') {
          const altGraph = document.getElementById('altitude-graph')
          const temp = document.getElementById('temp')
          temp.classList.remove('active')
          // graph no show
          altGraph.classList.remove('noShowGraph')
        }
        if (targetButton === 'rssi') {
          const rssiGraph = document.getElementById('rssi-graph')
          const hum = document.getElementById('hum')
          hum.classList.remove('active')
          // graph no show
          rssiGraph.classList.remove('noShowGraph')
        }
      }
      if (targetClassParent !== null) {
        event.target.parentNode.classList.add('active')
        if (targetClassParent === 'temp') {
          const altGraph = document.getElementById('altitude-graph')
          const alt = document.getElementById('alt')
          alt.classList.remove('active')
          // graph no show
          altGraph.classList.add('noShowGraph')
        }
        if (targetClassParent === 'hum') {
          const rssiGraph = document.getElementById('rssi-graph')
          const rssi = document.getElementById('rssi')
          rssi.classList.remove('active')
          // graph no show
          rssiGraph.classList.add('noShowGraph')
        }
        if (targetClassParent === 'alt') {
          const altGraph = document.getElementById('altitude-graph')
          const temp = document.getElementById('temp')
          temp.classList.remove('active')
          // graph no show
          altGraph.classList.remove('noShowGraph')
        }
        if (targetClassParent === 'rssi') {
          const rssiGraph = document.getElementById('rssi-graph')
          const hum = document.getElementById('hum')
          hum.classList.remove('active')
          // graph no show
          rssiGraph.classList.remove('noShowGraph')
        }
      }
    }
  }
}
</script>

<style>
  #nav{
    position: absolute;
    z-index: 1000;
    background: #667db6;  /* fallback for old browsers */
    background: -webkit-linear-gradient(to right, #667db6, #0082c8, #0082c8, #667db6) !important;  /* Chrome 10-25, Safari 5.1-6 */
    background: linear-gradient(to right, #667db6, #0082c8, #0082c8, #667db6) !important;
  }
  a {
    color: inherit;
    text-decoration: none;
  }
  .graph-button {
    margin: 0 4px;
    z-index: 10;
  }
  .active {
    background-color: #76FF03 !important;
  }
  .noShowGraph {
    z-index: -1 !important;
  }
  @media only screen and (max-width: 550px) {
    #alt {
      position: absolute;
      top: 47.5em;
      left: 12em;
    }
    #rssi {
      position: absolute;
      top: 47.5em;
      left: 17em;
    }
    #temp {
      position: absolute;
      top: 47.5em;
      left: 22.3em;
    }
    #hum {
      position: absolute;
      top: 47.5em;
      left: 28.25em;
    }
  }
</style>