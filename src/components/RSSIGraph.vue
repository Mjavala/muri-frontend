<template>
  <div id="rssi-graph">
        <rsssiReactivity :chart="chart" />
  </div>
</template>

<script>
import rsssiReactivity from './RSSIReactivity'

export default {
    components: {
        rsssiReactivity
    },
    props: [
      'idList', 'filteredRSSI'
    ],
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
        if (newVal.length > oldVal.length){
          // new device detected, add trace
          this.addTrace()
          this.findTrace(newVal)
        }
        if (newVal.length < 1){
          // first device
          this.chart.traces[0].name = this.currentDevice
        }
        if (newVal.length === 1){
          // first device
          if (this.count === 0){
            this.addTrace()
          }
        }
      }
    },
    data() {
    return {
      rssi: Number,
      currentDevice: '',
      count: 0,
      chart: {
        uuid: "1233",
        traces: [],
        layout: {
          height: 325,
          title: 'RSSI vs Time',
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
      addData (rssi, traceIndex) {
        this.chart.layout.datarevision = new Date().getTime();
        this.chart.traces[traceIndex].y.push(rssi);
        let time = new Date()
        this.chart.traces[traceIndex].x.push(time);
        if (this.chart.traces[traceIndex].x.length === 360){
          this.chart.traces[traceIndex].x.shift()
          this.chart.traces[traceIndex].y.shift()
        }
      },
      findTrace (deviceList) {
        for (const [i, id] of deviceList.entries()){
          if (id === this.currentDevice){
            this.addData(this.rssi, i)
          }
        }
      },
      addTrace () {
        const traceObj = {
            y: [],
            x: [new Date()],
            type: 'scatter',
            mode: 'lines+markers',
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
        display: inline-block;
        position: absolute;
        top: 47.5%;
    }
</style>