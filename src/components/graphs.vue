<template>
    <div class="wrapper">
        <Plotly  class="graph" :data="data" :layout="layout" :display-mode-bar="false"></Plotly>
    </div>
</template>

<script>
import { Plotly } from 'vue-plotly'

export default {
  components: {
    Plotly
  },
  data () {
    return {
        data:[{
        x: [1,2,3,4],
        y: [10,15,13,17],
        type:"scatter"
    }],
        layout: {
            title: "altitude",
            height: 400
            }
        }
    }
}
</script>

<style scoped>
    .wrapper{
        display: inline-block;
        position: absolute;
        top: 0;
        width: 45vw;
    }
</style>