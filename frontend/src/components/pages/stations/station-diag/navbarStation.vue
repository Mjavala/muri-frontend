<template>    
    <v-app-bar
        app
        dark
        id="nav"
    >
      <v-img id="iriss-logo" max-height="100" max-width="225" src="../../../../assets/iriss_logo.jpg" />
      <v-spacer />
      <v-btn class="spacing-nav" light small>
        <router-link to="/">Home</router-link>
      </v-btn>
      <v-btn id="station-diagnostics" light small @click="routeToDiagnostics">
        Station Data
      </v-btn>
    </v-app-bar>
</template>

<script>
export default {
  props: ['station'],
  watch: {
    station(newVal) {
      this.diagnostics = newVal
    }
  },
  data () {
    return {
      diagnostics: '',
    }
  },
  methods: {
    routeToDiagnostics(){
      let routeData = this.$router.resolve({name: 'station', params: {id: this.station}})
      window.open(routeData.href, '_blank')
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
  .spacing-nav {
    margin: 0 0.25em !important;
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
</style>