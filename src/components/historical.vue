<template>
  <div class="data-wrapper">
    <NavBar />
    <Loader v-if="show"></loader>
    <div id="data">
      {{this.muri_data}}
    </div>
  </div>
</template>

<script>
import NavBar from './navbar'
import Loader from './loader'
import gql from 'graphql-tag';

export default {
  components: {
    NavBar,
    Loader
  },
  data () {
    return {
      show: true,
      muri_data: {}
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
  },
  apollo: {
    muri_data: {
      query: gql`
         {
          muri_data (where: {time: {_gte: "2020-05-16T11:25:45.550641+00:00"}}) {
            altitude
            time
          }
        }`
      }
    }
  }

</script>

<style scoped>
  .data-wrapper {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>