<template>
  <div id="batt-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredBatteryMonitor'
    ],
    mounted () {
      let config = {displayModeBar: false, responsive: true}
      Plotly.react(
        'batt-graph',
        this.chart.traces,
        this.chart.layout,
        config
      )
    },
    watch: {
      filteredBatteryMonitor(newVal){
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        this.batt = objKeyMap[0]
      },
      idList(newVal, oldVal){
        if (newVal.length === oldVal.length){
          // current device message
          this.findTrace(newVal)
        }
        if (newVal.length > oldVal.length && newVal.length > 1){
          // new device detected, add trace
          this.addTrace(this.batt)
          this.findTrace(newVal)
        }
        if (newVal.length === 1){
          // first device
          if (this.counter === 0){
            this.timer = new Date()
            this.addTrace()
            this.counter = this.counter + 1
          }
        }
      }
    },
    data() {
    return {
      batt: Number,
      currentDevice: '',
      count: 0,
      timer: Number,
      counter: 0,
      chart: {
        uuid: "1234",
        traces: [],
        layout: {
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'Battery Monitor',
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
          showlegend: false,
          xaxis: {
            tickmode: 'auto',
            gridcolor: '#bdbdbd',
            gridwidth: 1,
            rangemode: 'tozero',
            showline:  true,
            zeroline: false,
            tickfont:{
              size: 8
            }
          },
          yaxis: {
            zeroline: false,
            showline:  true,
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
      addData (batt, traceIndex) {
        /* extend trace throttle ~
        let last = this.chart.traces[traceIndex].y[this.chart.traces[traceIndex].y.length - 1]
        if (last === humidity){
          this.count = this.count + 1
        }
        if (last !== humidity || this.count === 10) {
          this.count = 1
        } */
        const update = {
          x: [[new Date()]],
          y: [[batt]]
        }
        Plotly.extendTraces(
          'batt-graph',
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
            this.addData(this.batt, i)
          }
        }
      },
      addTrace (batt) {
        const traceObj = {
            y: [batt],
            x: [new Date()],
            type: 'scattergl',
            mode: 'lines',
            connectgaps: true,
            name: this.currentDevice
        }
        this.chart.traces.push(traceObj)
      },
    }
  }
</script>

<style scoped>
  #batt-graph{
    display: inline;
    position: absolute;
    top: 35%;
    left: 70%;
    width: 30%;
    height: 34%;
    z-index: 10;
  }
</style>