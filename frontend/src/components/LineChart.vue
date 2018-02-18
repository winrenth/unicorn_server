<script>
    import { Line, mixins } from 'vue-chartjs'
    export default {
        extends: Line,
        watch: {
            'chartData': {
                deep: true,
                handler (newData, oldData) {
                    if (!oldData)
                        return;
                    const chart = this.$data._chart;
                    if (chart) {
                        for (let i = 0; i < chart.data.datasets.length; i++) {
                            chart.data.datasets[i].data = newData.datasets[i].data;
                            chart.data.datasets[i].label = newData.datasets[i].label;
                        }
                        chart.update()
                    }
                    console.log(chart)
                    // this.renderChart(JSON.parse(JSON.stringify(newData)), this.options)
                }
            }
        },
        props: ['options', 'chartData'],
        mounted () {
            // this.chartData is created in the mixin.
            // If you want to pass options please create a local options object
            this.renderChart(JSON.parse(JSON.stringify(this.chartData)), this.options)
        }
    }
</script>
