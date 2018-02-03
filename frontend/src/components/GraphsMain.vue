<template>
    <div>
        <div class='row'>
            <graph-card
                    v-for='(m, prop) in measured'
                    :key="prop"
                    :name='prop'
                    :results='m'
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
                    'temperature': []
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
                        let fakeData = {
                            Calls: [1, 2],
                            Summary: {
                                Calls: 3,
                                Available: 0,
                                WaitTime: 0,
                                TalkTime: 0
                            },
                            Members: [
                                {Name: 109, Status: 1},
                                {Name: 101, Status: 2},
                                {Name: 102, Status: 3}
                            ]
                        };
                        this.processResponse(fakeData)
                    })
            },
            processResponse(data) {
                this.stations = [];
                let that = this;
                console.log(data);

                _.each(data, function (station) {
                    station.results = [];
                    that.$http.get(`${apiResults}/${station.name}`, data = {data})
                        .then(response => {
                            // JSON responses are automatically parsed.
                            station.results.push(response.data);
                            that.getMeasuredSeries(response.data);
                        }).catch(e => {
                            console.log(e);
                            // that.errors.push(e)
                        });
                    that.stations.push(station);
                })
                /*
                for (let member of data.Members) {
                  this.$root.db.get(`user_${member.Name}`).catch(function (err) {
                    if (err.name === 'not_found') {
                      return {
                        name: 'Unknown', photo: require('assets/dummy.jpg')
                      };
                    } else {
                      throw err;
                    }
                  }).then(function (user) {
                    that.$root.db.get(`status_${member.Status}`).then(function (status) {
                      that.cards.push({
                        ...user,
                        ...status
                      })
                    })
                  }).catch(function (err) {
                    console.log(err)
                  });
                }
                */
            },
            getMeasuredSeries(data) {
                let temp = _.chain(data)
                    .map(_.partialRight(_.pick, 'timestamp', 'temperature'))
                    .value();
                let name = data[0].name;
                this.measured.temperature.push({
                    name: temp
                });
            }
        },
        mounted() {
            this.loadData();

            this.interval = setInterval(function () {
                this.loadData();
            }.bind(this), 3000);
        },

        beforeDestroy() {
            clearInterval(this.interval);
        }
    }
</script>

<style lang='stylus' scoped>
    .card
        width: 15%
        min-width: 300px
</style>
