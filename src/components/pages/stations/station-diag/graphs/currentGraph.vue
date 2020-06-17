<template>
  <div id="current-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredCurrent'
    ],
    mounted () {
      let config = {displayModeBar: false, responsive: true}
      Plotly.react(
        'current-graph',
        this.chart.traces,
        this.chart.layout,
        config
      )
    },
    watch: {
      filteredCurrent(newVal){
        if (this.statMessageCount === 0) {
          this.statMessageCount = this.statMessageCount + 1
        }
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        this.current = objKeyMap[0]
        if (this.counter === 0 && this.statMessageCount === 1) {
          this.timer = new Date()
          this.addTrace(this.current)
          this.counter = this.counter + 1
        } else {
          this.addData(this.current)
        }
      }
    },
    data() {
    return {
      current: Number,
      currentDevice: '',
      timer: Number,
      count: 0,
      counter: 0,
      statMessageCount: 0,
      chart: {
        uuid: "1233",
        traces: [],
        layout: {
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'Current vs Time',
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
              text: 'Current',
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
      addData (current) {
        const update = {
          x: [[new Date()]],
          y: [[current]]
        }
        Plotly.extendTraces(
          'current-graph',
          update, 
          [0],  // only 1 station
        )
        const newTime = new Date()
        const delta =  (newTime - this.timer) / 1000
        if (delta >= 1800) {
          // 30 minute timeframe reached, need to remove first element of array as new one gets added
          this.chart.traces[0].y.shift()
          this.chart.traces[0].x.shift()
        }
      },
      addTrace (current) {
        const traceObj = {
            y: [current],
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
  #current-graph{
    display: inline;
    position: absolute;
    top: 42%;
    left: 51%;
    width: 45%;
    height: 35%;
    z-index: 10;
  }
</style>