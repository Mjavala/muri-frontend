<template>
  <div id="temp-graph">
        <temperatureReactivity :chart="chart" />
  </div>
</template>

<script>
import temperatureReactivity from './temperatureReactivity.vue'
export default {
    components: {
        temperatureReactivity
    },
    props: [
      'idList', 'filteredTemp'
    ],
    watch: {
      filteredTemp(newVal){
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        let temp = objKeyMap[0] / 1000
        this.temp = temp
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
          this.addTrace()
        }
      }
    },
    data() {
    return {
      temp: Number,
      currentDevice: '',
      showlegend: false,
      count: 0,
      chart: {
        uuid: "12345",
        traces: [],
        layout: {
          height: 325 ,
          title: 'Temperature vs Time',
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
            title: 'Temp (K)',
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
      addData (temp, traceIndex) {
        this.count = this.count + 1
        if (this.count === 2) {
          this.chart.layout.datarevision = new Date().getTime();
          this.chart.traces[traceIndex].y.push(temp);
          let time = new Date()
          this.chart.traces[traceIndex].x.push(time);
          if (this.chart.traces[traceIndex].x.length === 360){
            this.chart.traces[traceIndex].x.shift()
            this.chart.traces[traceIndex].y.shift()
          }
          this.count = 0
        }
      },
      findTrace (deviceList) {
        for (const [i, id] of deviceList.entries()){
          if (id === this.currentDevice){
            this.addData(this.temp, i)
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
    #temp-graph{
        display: inline-block;
        position: absolute;
        top: 0%;
        width: 50%;
    }
  @media only screen and (max-width: 768px) {
    #temp-graph {
      display: block;
      position: relative;
      width: 100%;
    }
  }
</style>