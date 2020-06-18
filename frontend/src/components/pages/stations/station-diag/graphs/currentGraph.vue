<template>
  <div id="azm-elv-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [ 
      'filteredElevation', 'filteredAzimuth'
    ],
    mounted () {
      let config = {displayModeBar: false, responsive: true}
      Plotly.react(
        'azm-elv-graph',
        this.chart.traces,
        this.chart.layout,
        config
      )
    },
    watch: {
      filteredAzimuth(newVal){
        if (this.statMessageCount === 0) {
          this.statMessageCount = this.statMessageCount + 1
        }
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        this.az = objKeyMap[0]
        if (this.counter === 0 && this.statMessageCount === 1) {
          this.timer = new Date()
          this.addTrace(this.az, 'az')
          this.counter = this.counter + 1
        } else {
          this.addData(this.az)
        }
      },
      filteredElevation(newVal){
        if (this.statMessageCount1 === 0) {
          this.statMessageCount1 = this.statMessageCount1 + 1
        }
        let objKey = Object.keys(newVal)
        this.currentDevice1 = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        this.elv = objKeyMap[0]
        if (this.counter1 === 0 && this.statMessageCount1 === 1) {
          this.addTrace(this.elv, 'elv')
          this.counter1 = this.counter1 + 1
        } else {
          this.addDataElv(this.elv)
        }
      }
    },
    data() {
    return {
      az: Number,
      elv: Number,
      currentDevice: '',
      currentDevice1: '',
      timer: Number,
      counter: 0,
      counter1: 0,
      statMessageCount: 0,
      statMessageCount1: 0,
      chart: {
        uuid: "1233",
        traces: [],
        layout: {
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'Azimuth & Elevation',
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
      addData (point) {
        const update = {
          x: [[new Date()]],
          y: [[point]]
        }
        Plotly.extendTraces(
          'azm-elv-graph',
          update, 
          [0],  // only 1 station
        )
        const newTime = new Date()
        const delta =  (newTime - this.timer) / 1000
        if (delta >= 1800) {
          // 30 minute timeframe reached, need to remove first element of array as new one gets added
          this.chart.traces[0].y.shift()
          this.chart.traces[0].x.shift()
          this.chart.traces[1].y.shift()
          this.chart.traces[1].x.shift()
        }
      },
      addDataElv (point) {
        const update = {
          x: [[new Date()]],
          y: [[point]]
        }
        Plotly.extendTraces(
          'azm-elv-graph',
          update, 
          [1],  // repeating yourself cuz you suuuuuuuuck ~ deadlineisbelikedeadlinedo ~
        )
      },
      addTrace (point, name) {
        const traceObj = {
            y: [point],
            x: [new Date()],
            type: 'scattergl',
            mode: 'lines',
            connectgaps: true,
            name: name
        }
        this.chart.traces.push(traceObj)
      },
    }
  }
</script>

<style scoped>
  #azm-elv-graph{
    display: inline;
    position: absolute;
    top: 42%;
    left: 51%;
    width: 45%;
    height: 35%;
    z-index: 10;
  }
</style>