<template>
    <v-app>
    <div id="home-wrap">
        <navbar :station="station" :live="live"/>
        <mqttReceiver @stations="newStationListFunc" @live="mqttConnected"/>
        <div id="stations-dropdown">
            <v-select
                :items="items"
                label="Available Stations"
                filled
                v-model="station"
            ></v-select>
        </div>
    </div>
    </v-app>
</template>

<script>
import navbar from './navbarHome'
import mqttReceiver from './mqttReceiver'

export default {
    components: {
        navbar, 
        mqttReceiver
    },
    watch: {
        newStationList(newVal) {
            this.items = newVal
        }
    },
    methods: {
        newStationListFunc(data){
            this.newStationList = data
        },
        mqttConnected(data) {
            this.live = data
        }
    },
    data () {
        return {
            items: [],
            newStationList: [],
            station: '',
            live: false
        }
    }
}
</script>

<style scoped>
    a {
        color: inherit;
        text-decoration: none;
    }
    #home-wrap {
        position: relative;
    }
    #stations-dropdown {
        width: 20vw;
        position: absolute;
        top: 10%;
        right: 5%;
    }
    #station-button {
        position: absolute;
        top: 50%;
        left: 89%;
        z-index: 10000000;
    }
    #stations {
        z-index: 10;
    }
</style>