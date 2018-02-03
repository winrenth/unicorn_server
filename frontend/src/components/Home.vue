<template>
    <!-- Configure "view" prop for QLayout -->
    <q-layout view="lHh Lpr lFf">
        <!-- Navigation Tabs   -->
        <q-tabs slot="navigation" align="justify" color="faded">
            <q-route-tab slot="title" icon="view_module" to="/" replace hide="icon" label="Live Queue" />
            <q-route-tab slot="title" icon="history" to="/layout/stats" replace hide="icon" label="Stats" />
        </q-tabs>

        <router-view />

        <!-- Footer  -->
        <q-toolbar slot="footer" color="faded">
            <q-toolbar-title class="text-right">
                &copy;{{year}} Lafiel
            </q-toolbar-title>
        </q-toolbar>
    </q-layout>
</template>

<script>
    import {
        QLayout,
        QTabs,
        QRouteTab,
        QToolbar,
        QToolbarTitle
    } from 'quasar'

    export default {
        name: 'index',
        components: {
            QLayout,
            QToolbar,
            QTabs,
            QRouteTab,
            QToolbarTitle
        },
        data() {
            return {
                'year': new Date().getFullYear()
            }
        }
    }
</script>

<style>
</style>
