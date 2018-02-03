<template>
    <q-card inline class="card" >
        <q-card-media overlay-position="bottom">
            <q-card-title slot="overlay" class="text-bold">
                {{ name }}
            </q-card-title>
        </q-card-media>
        <q-card-main>
            <p class="text-center">
                <line-chart :chart-data="datacollection"></line-chart>
                <button @click="fillData()">Randomize</button>
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
        QIcon
    } from 'quasar'
    import LineChart from './LineChart.vue'

    export default {
        name: 'index',
        components: {
            QCard,
            QCardTitle,
            QCardMain,
            QCardMedia,
            QIcon,
            LineChart
        },
        props: ['name', 'results'],
        data () {
            return {
                datacollection: null
            }
        },
        mounted () {
            this.fillData()
        },
        methods: {
            fillData () {
                console.log(this.results);
                this.datacollection = {
                    labels: [this.getRandomInt(), this.getRandomInt()],
                    datasets: [
                        {
                            label: 'Data One',
                            backgroundColor: '#f87979',
                            data: [this.getRandomInt(), this.getRandomInt()]
                        }, {
                            label: 'Data One',
                            backgroundColor: '#f87979',
                            data: [this.getRandomInt(), this.getRandomInt()]
                        }
                    ]
                }
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


export default {
extends: Line,
props: ['data', 'options'],
mounted () {
this.renderChart(this.data, this.options)
}
}
