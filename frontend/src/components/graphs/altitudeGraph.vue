<template>
  <div id="altitude-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredAltitude'
    ],
    mounted () {
      // let resp = {responsive: true}
      let config = {displayModeBar: false, responsive: true}
      Plotly.react(
        'altitude-graph',
        this.chart.traces,
        this.chart.layout,
        config

      )
    },
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
          // check timeframe
        }
        if (newVal.length > oldVal.length && newVal.length > 1){
          // new device detected, add trace
          this.addTrace(this.altitude)
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
      altitude: Number,
      currentDevice: '',
      throttleCount: 0,
      timer: Number,
      counter: 0,
      count: 0,
      chart: {
        uuid: "123",
        traces: [],
        layout: {
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'Altitude vs Time(s)',
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
            titlefont: {
              size: 10
            },
            tickfont:{
              size: 8
            }
          },
          yaxis: {
            title: {
              text: 'Altitude (m)',
              standoff: 20
            },
            zeroline: false,
            showline:  true,
            rangemode: 'tozero',
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
      addData (altitude, traceIndex) {
        // const t0 = new Date()
        const update = {
          x: [[new Date()]],
          y: [[altitude]]
        }
        Plotly.extendTraces(
          'altitude-graph',
          update,
          [traceIndex],
        )
        // const t1 = new Date()
        // console.log('took ' + (t1-t0) + 'miliseconds')
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
            this.addData(this.altitude, i)
          }
        }
      },
      addTrace (altitude) {
        const traceObj = {
            y: [altitude],
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
  #altitude-graph{
      display: inline;
      position: absolute;
      top: 5%;
      left: 49%;
      width: 25%;
      height: 35%;
      z-index: 10;
  } 
  @media only screen and (max-width: 768px) {
    #altitude-graph {
      display: block;
      position: relative;
      width: 100%;
    }
  }
</style>