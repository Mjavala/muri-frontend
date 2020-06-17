<template>
  <div id="cw-graph">
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist/plotly'

export default {
    props: [
      'idList', 'filteredCwAvgs'
    ],
    mounted () {
      let config = {displayModeBar: false, responsive: true}
      Plotly.react(
        'cw-graph',
        this.chart.traces,
        this.chart.layout,
        config
      )
    },
    watch: {
      filteredCwAvgs(newVal){
        // need slightly different setup for bar chart
        let objKey = Object.keys(newVal)
        this.currentDevice = objKey[0]
        let objKeyMap = Object.keys(newVal).map((k) => newVal[k]);
        let cwAverages = objKeyMap[0]
        this.cw = cwAverages
      },
      idList(newVal, oldVal){
        if (newVal.length === oldVal.length){
          // current device message
          this.findTrace(newVal)
          // check timeframe
        }
        if (newVal.length > oldVal.length && newVal.length > 1){
          // new device detected, add trace
          this.addTrace(this.cw)
          this.findTrace(newVal)
        }
        if (newVal.length === 1){
          // first device
          if (this.counter === 0) {
            this.timer = new Date()
            this.addTrace(this.cw)
            this.counter = this.counter + 1
          }
        }
      }
    },
    data() {
    return {
      cw: [],
      currentDevice: '',
      counter: 0,
      count: 0,
      chart: {
        uuid: "123",
        traces: [],
        layout: {
          plot_bgcolor: '#F5F5F5',
          title: {
            text: 'CW Spectral Averages',
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
            showline:  true,
            zeroline: false,
            gridwidth: 1,
            tickfont:{
              size: 8
            }
          },
          yaxis: {
            tickmode: 'auto',
            showline:  true,
            zeroline: false,
            gridwidth: 1,
            gridcolor: '#bdbdbd',
            tickfont:{
              size: 8
            }
          }
        }
      }
    }
    },
    methods: {
      addData (cw, traceIndex) {
        // only restyle if the data is different
        const update = {
          y: cw,
        }
        Plotly.animate(
          'cw-graph', {
            data: [update],
            layout: this.chart.layout,
            traces: [traceIndex]
          }, {
            transition: {duration: 0},
            frame: {duration: 0, redraw: false}
          })
      },
      findTrace (deviceList) {
        for (const [i, id] of deviceList.entries()){
          if (id === this.currentDevice){
            this.addData(this.cw, i)
          }
        }
      },
      addTrace (cw) {
        const traceObj = {
            y: cw,
            x: ['cw0','cw1', 'cw2', 'cw3', 'cw4', 'cw5', 'cw6', 'cw7', 'cw8'],
            type: 'bar',
            name: this.currentDevice
        }
        this.chart.traces.push(traceObj)
        Plotly.react(
          'cw-graph',
          this.chart.traces,
          this.chart.layout
        )
      }
    } 
  }
</script>

<style scoped>
    #cw-graph{
      display: inline;
      position: absolute;
      top: 81%;
      left: 74%;
      width: 25%;
      height: 35%;
      z-index: 10;
    }
  @media only screen and (max-width: 768px) {
    #cw-graph {
      display: block;
      position: relative;
      width: 100%;
    }
  }
</style>