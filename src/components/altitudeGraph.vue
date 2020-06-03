<template>
  <div id="altitude-graph">
        <altitudeReactivity :chart="chart" />
  </div>
</template>

<script>
import altitudeReactivity from './altitudeReactivity.vue'
export default {
    components: {
        altitudeReactivity
    },
    props: [
      'idList', 'filteredAltitude'
    ],
    watch: {
      filteredAltitude(newVal){
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        let altitude = objKeyMap[0] / 1000
        this.altitude = altitude
      },
      idList(newVal, oldVal){
        if (newVal.length === oldVal.length){
          // current device message
          this.findTrace(newVal)
        }
        if (newVal.length > oldVal.length){
          // new device detected, add trace
          this.addTrace()
          this.findTrace(newVal)
        }
        if (newVal.length === 1){
          // first device
          if (this.count === 0){
            this.addTrace()
          }
        }
      }
    },
    data() {
    return {
      altitude: Number,
      count: 0,
      currentDevice: '',
      showlegend: false,
      chart: {
        uuid: "123",
        traces: [],
        layout: {
          height: 325 ,
          title: 'Altitude vs Time',
          xaxis: {
            tickmode: 'auto',
            gridcolor: '#bdbdbd',
            gridwidth: 1,
            title: 'time (s)',
            titlefont: {
              size: 11
            },
            tickfont:{
              size: 10
            }
          },
          yaxis: {
            title: 'Altitude (m)',
            titlefont: {
              size: 11
            },
            gridwidth: 1,
            gridcolor: '#bdbdbd',
          }
        }
      }
    }
    },
    methods: {
      addData (altitude, traceIndex) {
        this.chart.layout.datarevision = new Date().getTime();
        this.chart.traces[traceIndex].y.push(altitude);
        let time = new Date()
        this.chart.traces[traceIndex].x.push(time);
        if (this.chart.traces[traceIndex].x.length === 360){
          this.chart.traces[traceIndex].x.shift()
          this.chart.traces[traceIndex].y.shift()
        }
      },
      findTrace (deviceList) {
        for (const [i, id] of deviceList.entries()){
          if (id === this.currentDevice){
            this.addData(this.altitude, i)
          }
        }
      },
      addTrace () {
        const traceObj = {
            y: [],
            x: [new Date()],
            type: 'scatter',
            mode: 'lines+markers',
            connectgaps: true,
            name: this.currentDevice
        }
        this.chart.traces.push(traceObj)
      }
    } 
  }
</script>

<style scoped>
    #altitude-graph{
        display: inline-block;
        position: absolute;
        top: 0%;
    }

</style>