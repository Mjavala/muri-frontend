<template>
    <div :ref="chart.uuid"></div>
</template>
<script>
import Plotly from 'plotly.js-dist/plotly'
export default {
  props: ["chart"],
  mounted() {
    const config = {responsive: true}
    Plotly.plot(this.$refs[this.chart.uuid], this.chart.traces, this.chart.layout, config);
  },
  watch: {
    chart: {
      handler: function() {
        Plotly.react(
          this.$refs[this.chart.uuid],
          this.chart.traces,
          this.chart.layout
        );        
      },
      deep: true
    }
  } 
}
</script>
