<template>
    <q-card inline class="card" >
        <q-card-media overlay-position="bottom">
            <q-card-title slot="overlay" class="text-bold">
                {{ name }}
            </q-card-title>
        </q-card-media>
        <q-card-main>
            <p class="text-center">
                <line-chart :chart-data="chartData" :options="options"></line-chart>
                <q-btn @click="fillData()">Randomize</q-btn>
            </p>
            <div class="text-center">{{ name }}</div>

        </q-card-main>
    </q-card>
</template>

<script>
    import {
        QCard,
        QCardTitle,
        QCardMain,
        QCardMedia,
        QBtn,
        QIcon
    } from 'quasar'
    import moment from 'moment'
    import LineChart from './LineChart.vue'

    const
        _ = require('lodash');

    function newDate(days) {
        return moment().add(days, 'd').toDate();
    }

    function newDateString(days) {
        return moment().add(days, 'd').format();
    }
    export default {
        name: 'index',
        components: {
            QCard,
            QBtn,
            QCardTitle,
            QCardMain,
            QCardMedia,
            QIcon,
            LineChart
        },
        props: ['name', 'results', 'stations'],
        data: () => ({
            chartData: {
                datasets: [{
                    label: 'Dataset with string point data',
                    backgroundColor: 'red',
                    borderColor: 'black',
                    fill: false,
                    data: []
                }, {
                    label: 'Dataset with date object point data',
                    backgroundColor: 'green',
                    borderColor: 'gray',
                    fill: false,
                    data: []
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: ''
                },
                scales: {
                    xAxes: [{
                        type: 'time',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'
                        },
                        ticks: {
                            major: {
                                fontStyle: 'bold',
                                fontColor: '#FF0000'
                            }
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'value'
                        }
                    }]
                }
            }
        }),

        mounted () {
            this.fillData();
        },
        watch: {
            // whenever question changes, this function will run
            results: function (newResults, oldResults) {
                if (this.stations) {
                    this.fillData();
                }
            }
        },
        methods: {
            fillData2() {
                console.log(this.chartData.datasets[0].data[0].y);
                this.chartData.datasets[0].data[0].y = Math.round(Math.random() * 10);
                console.log(this.chartData.datasets[0].data[0].y)
            },
            fillData() {
                let i = 0, min_ts = 0;
                let that = this;
                _.each(this.results, function(dataset) {
                    min_ts = min_ts < dataset[0].timestamp ? dataset[0].timestamp : min_ts;
                });
                min_ts -= 60 * 60 * 8; // max 8h offset
                _.each(this.results, function(dataset) {
                    if (!that.chartData.datasets[i]) {
                        that.chartData.datasets.push({data: []});
                    }
                    that.chartData.datasets[i].label = that.stations[i].name;
                    let j = 0;
                    _.each(dataset, function(result) {
                        if (result.timestamp > min_ts) {
                            if (that.chartData.datasets[i].data[j]) {
                                that.chartData.datasets[i].data[j].y = result[that.name];
                                that.chartData.datasets[i].data[j].x = moment.unix(result.timestamp);
                            } else {
                                that.chartData.datasets[i].data.push(
                                    {
                                        y: result[that.name],
                                        x: moment.unix(result.timestamp)
                                    }
                                )
                            }
                        }
                        j += 1;
                    });
                    i += 1;
                });
                // this.chartData.datasets[0].data[0].y = Math.round(Math.random() * 10);
            },
            getRandomInt () {
                return Math.floor(Math.random() * (50 - 5 + 1)) + 5
            }
        }
    }
</script>

<style lang="stylus" scoped>
    .outer
        overflow: hidden;

    .img-photo
        height: 100%
        width: auto
        max-height: 300px
        margin-left: 50%;
        transform: translateX(-50%);
        vertical-align: middle



</style>
