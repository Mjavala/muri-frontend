<template>
  <div id="rssi-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredRSSI'
    ],
    mounted () {
      let config = {displayModeBar: false, responsive: true}
      Plotly.react(
        'rssi-graph',
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
        this.rssi = objKeyMap[0]
      },
      idList(newVal, oldVal){
        if (newVal.length === oldVal.length){
          // current device message
          this.findTrace(newVal)
        }
        if (newVal.length > oldVal.length && newVal.length > 1){
          // new device detected, add trace
          this.addTrace(this.rssi)
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
      rssi: Number,
      currentDevice: '',
      timer: Number,
      count: 0,
      counter: 0,
      chart: {
        uuid: "1233",
        traces: [],
        layout: {
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'RSSI vs Time',
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
            rangemode: 'tozero',
            showline:  true,
            zeroline: false,
            gridwidth: 1,
            tickfont:{
              size: 8
            }
          },
          yaxis: {
            zeroline: false,
            showline:  true,
            rangemode: 'tozero',
            title: {
              text: 'RSSI',
              standoff: 20
            },
            titlefont: {
              size: 9
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
      addData (rssi, traceIndex) {
        /*let last = this.chart.traces[traceIndex].y[this.chart.traces[traceIndex].y.length - 1]
        if (last === rssi){
          this.count = this.count + 1
        }
        if (last !== rssi || this.count === 10) { 
          this.count = 1
        }*/
        const update = {
          x: [[new Date()]],
          y: [[rssi]]
        }
        Plotly.extendTraces(
          'rssi-graph',
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
            this.addData(this.rssi, i)
          }
        }
      },
      addTrace (rssi) {
        const traceObj = {
            y: [rssi],
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
  #rssi-graph{
    display: inline;
    position: absolute;
    top: 45%;
    left: 49%;
    width: 25%;
    height: 35%;
    z-index: 10;
  }
  @media only screen and (max-width: 768px) {
    #rssi-graph {
      display: block;
      position: relative;
      width: 100%;
    }
  }
</style>