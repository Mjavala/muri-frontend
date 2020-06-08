<template>
  <div id="hum-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredHum'
    ],
    mounted () {
      let config = {responsive: true}
      Plotly.react(
        'hum-graph',
        this.chart.traces,
        this.chart.layout,
        config
      )
    },
    watch: {
      filteredHum(newVal){
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        this.humidity = objKeyMap[0]
      },
      idList(newVal, oldVal){
        if (newVal.length === oldVal.length){
          // current device message
          this.findTrace(newVal)
        }
        if (newVal.length > oldVal.length && newVal.length > 1){
          // new device detected, add trace
          this.addTrace(this.humidity)
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
      humidity: Number,
      currentDevice: '',
      count: 0,
      timer: Number,
      counter: 0,
      chart: {
        uuid: "1234",
        traces: [],
        layout: {
          height: 325,
          title: 'Humidity vs Time',
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
            title: 'RSSI',
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
      addData (humidity, traceIndex) {
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
          y: [[humidity]]
        }
        Plotly.extendTraces(
          'hum-graph',
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
            this.addData(this.humidity, i)
          }
        }
      },
      addTrace (humidity) {
        const traceObj = {
            y: [humidity],
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
  #hum-graph{
    display: inline-block;
    position: absolute;
    top: 47.5%;
    width: 50%;
  }
  @media only screen and (max-width: 768px) {
    #hum-graph {
      display: block;
      position: relative;
      width: 100%;
    }
  }
</style>