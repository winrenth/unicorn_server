<template>
    <div>
        <div class='row'>
            <graph-card
                    v-for='(m, prop) in measured'
                    :key="prop"
                    :name='prop'
                    :results='m'
                    :stations='stations'
            ></graph-card>
        </div>
    </div>
</template>

<script>
    import GraphCard from './GraphCard.vue'

    const
        apiStations = '/api/stations',
        apiResults = '/api/data',
        _ = require('lodash');

    export default {
        name: 'index',
        components: {
            GraphCard
        },
        data() {
            return {
                interval: null,
                stations: [],
                measured: {
                    'temperature': [],
                    'pressure': [],
                    'humidity': [],
                    'light': [],
                    'battery': [],
                    'CO2': []
                },
                bar: {
                    waiting: 0,
                    talking: 0,
                    idle: 0,
                    avgWait: 0,
                    avgTalk: 0
                }
            }
        },
        methods: {
            loadData() {
                let data = {
                    extno: 0
                };
                this.$http.get(apiStations, data = {data})
                    .then(response => {
                        // JSON responses are automatically parsed.
                        this.processResponse(response.data);
                    })
                    .catch(e => {
                        console.log(e);
                        // this.errors.push(e)
                        let fakeData = {};
                        this.processResponse(fakeData)
                    })
            },
            processResponse(data) {
                this.stations = [];
                let that = this;
                this.measured.temperature = [];
                _.each(data, function (station) {
                    station.results = [];
                    that.$http.get(`${apiResults}/${station.name}`, data = {data})
                        .then(response => {
                            // JSON responses are automatically parsed.
                            station.results.push(response.data);
                            that.getMeasuredSeries(response.data, that.stations.length - 1);
                        }).catch(e => {
                            console.log(e);
                            // that.errors.push(e)
                        });
                    that.stations.push(station);
                })
            },
            getMeasuredSeries(data, station_no) {
                let temp = _.chain(data)
                    .map(_.partialRight(_.pick, 'timestamp', 'temperature'))
                    .value();
                let pressure = _.chain(data)
                    .map(_.partialRight(_.pick, 'timestamp', 'pressure'))
                    .value();
                let humidity = _.chain(data)
                    .map(_.partialRight(_.pick, 'timestamp', 'humidity'))
                    .value();
                let light = _.chain(data)
                    .map(_.partialRight(_.pick, 'timestamp', 'light'))
                    .value();
                let battery = _.chain(data)
                    .map(_.partialRight(_.pick, 'timestamp', 'battery'))
                    .value();
                let CO2 = _.chain(data)
                    .map(_.partialRight(_.pick, 'timestamp', 'CO2'))
                    .value();
                let name = data[0].name;
                if (this.measured.temperature[station_no]) {
                    this.measured.temperature[station_no] = temp;
                } else {
                    this.measured.temperature.push(temp);
                }
                if (this.measured.pressure[station_no]) {
                    this.measured.pressure[station_no] = pressure;
                } else {
                    this.measured.pressure.push(pressure);
                }
                if (this.measured.humidity[station_no]) {
                    this.measured.humidity[station_no] = humidity;
                } else {
                    this.measured.humidity.push(humidity);
                }
                if (this.measured.light[station_no]) {
                    this.measured.light[station_no] = light;
                } else {
                    this.measured.light.push(light);
                }
                if (this.measured.battery[station_no]) {
                    this.measured.battery[station_no] = battery;
                } else {
                    this.measured.battery.push(battery);
                }
                if (this.measured.CO2[station_no]) {
                    this.measured.CO2[station_no] = CO2;
                } else {
                    this.measured.CO2.push(CO2);
                }
            }
        },
        mounted() {
            this.loadData();

            this.interval = setInterval(function () {
                this.loadData();
            }.bind(this), 30000);
        },

        beforeDestroy() {
            clearInterval(this.interval);
        }
    }
</script>

<style lang='stylus' scoped>
    .card
        width: 48%
        min-width: 300px
</style>
