<template>
  <div id="temp-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredTemp'
    ],
    mounted () {
      let config = {displayModeBar: false, responsive: true}
      Plotly.react(
        'temp-graph',
        this.chart.traces,
        this.chart.layout,
        config
      )
    },
    watch: {
      filteredTemp(newVal){
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        let temp = objKeyMap[0]
        this.temp = temp
      },
      idList(newVal, oldVal){
        if (newVal.length === oldVal.length){
          // current device message
          this.findTrace(newVal)
        }
        if (newVal.length > oldVal.length && newVal.length > 1){
          // new device detected, add trace
          this.addTrace(this.temp)
          this.findTrace(newVal)
        }
        if (newVal.length === 1){
          // first device
          if (this.counter === 0) {
            this.timer = new Date()
            this.addTrace()
            this.counter = this.counter + 1
          }
        }
      }
    },
    data() {
    return {
      temp: Number,
      currentDevice: '',
      timer: Number,
      count: 0,
      counter: 0,
      chart: {
        uuid: "12345",
        traces: [],
        layout: {
          showlegend: false,
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'Temp vs Time',
            font: {
              size: 11
            }
          },
          margin: {
            t: 17.5,
            b: 25,
            r: 20,
            l: 35
          },
          xaxis: {
            tickmode: 'auto',
            gridcolor: '#bdbdbd',
            gridwidth: 1,
            showline:  true,
            zeroline: false,
            rangemode: 'tozero',
            tickfont:{
              size: 8
            }
          },
          yaxis: {
            title: 'Temp (C)',
            showline:  true,
            zeroline: false,
            rangemode: 'tozero',
            titlefont: {
              size: 10
            },
            tickfont:{
              size: 8
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
        /*let last = this.chart.traces[traceIndex].y[this.chart.traces[traceIndex].y.length - 1]
        if (last === temp){
          this.count = this.count + 1
        }
        if (last !== temp || this.count === 10) { 
          this.count = 1 
          } */
        const update = {
          x: [[new Date()]],
          y: [[temp]]
        }
        Plotly.extendTraces(
          'temp-graph',
          update, 
          [traceIndex],
        )
        const newTime = new Date()
        const delta =  (newTime - this.timer) / 1000
        if (delta >= 1800) {
          // 30 minute timeframe reached, need to remove first element of array as new one gets added
          this.chart.traces[traceIndex].y.shift()
          this.chart.traces[traceIndex].x.shift()
        }
      },
      findTrace (deviceList) {
        for (const [i, id] of deviceList.entries()){
          if (id === this.currentDevice){
            this.addData(this.temp, i)
          }
        }
      },
      addTrace (temp) {
        const traceObj = {
            y: [temp],
            x: [new Date()],
            type: 'scattergl',
            mode: 'lines',
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
    display: inline;
    position: absolute;
    top: 0;
    left: 70%;
    width: 30%;
    height: 34%;
    z-index: 100;
  } 
</style>