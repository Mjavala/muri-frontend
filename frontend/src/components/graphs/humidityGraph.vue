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
      let config = {displayModeBar: false, responsive: true}
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
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'Humidity vs Time',
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
            title: {
              text: 'Humidity',
              standoff: 20
            },
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
    display: inline;
    position: absolute;
    top: 45%;
    left: 74%;
    width: 25%;
    height: 35%;
    z-index: 10;
  }
  @media only screen and (max-width: 768px) {
    #hum-graph {
      display: block;
      position: relative;
      width: 100%;
    }
  }
</style>