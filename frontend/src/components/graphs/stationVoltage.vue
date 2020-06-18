<template>
  <div id="volt-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredVoltage'
    ],
    mounted () {
      let config = {responsive: true}
      Plotly.react(
        'volt-graph',
        this.chart.traces,
        this.chart.layout,
        config
      )
    },
    watch: {
      filteredRSSI(newVal){
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        this.volt = objKeyMap[0]
      },
      idList(newVal, oldVal){
        if (newVal.length === oldVal.length){
          // current device message
          this.findTrace(newVal)
        }
        if (newVal.length > oldVal.length && newVal.length > 1){
          // new device detected, add trace
          this.addTrace(this.volt)
          this.findTrace(newVal)
        }
        if (newVal.length < 1){
          // first device
          this.chart.traces[0].name = this.currentDevice
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
      volt: Number,
      currentDevice: '',
      timer: Number,
      count: 0,
      counter: 0,
      chart: {
        uuid: "1233",
        traces: [],
        layout: {
          height: 325,
          title: 'Voltage vs Time',
          showlegend: false,
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
            title: 'Voltage',
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
      addData (volt, traceIndex) {
        // ~ throttling logic ~
        /*let last = this.chart.traces[traceIndex].y[this.chart.traces[traceIndex].y.length - 1]
        if (last === rssi){
          this.count = this.count + 1
        }
        if (last !== rssi || this.count === 10) { 
          this.count = 1
        }*/
        const update = {
          x: [[new Date()]],
          y: [[volt]]
        }
        Plotly.extendTraces(
          'volt-graph',
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
            this.addData(this.volt, i)
          }
        }
      },
      addTrace (volt) {
        const traceObj = {
            y: [volt],
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
  #volt-graph{
    display: inline-block;
    position: absolute;
    top: 47.5%;
    width: 50%;
    z-index: 10;
  }
</style>