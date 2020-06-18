<template>
    <div>
        <v-card id="positional-card" flat>
            <v-card-title id="position-title">Station positional info</v-card-title>
            <v-data-table disable-sort dense hide-default-footer :headers="headers" :items="info" item-key="name"></v-data-table>
        </v-card>
    </div>
</template>

<script>
export default {
    props: ['stationTrackingInfoMessage'],
    watch: {
        stationTrackingInfoMessage (newVal) {
            this.payload = newVal
            this.parseAndSetValues(this.payload)            
        }
    },
    data () {
        return {
            payload: '',
            info: [{
                lat: 105,
                lon: 39,
                alt: 17000,
                gps_numsats: 1000,
            }],
            headers: [
                { text: 'lat', value: 'lat' },
                { text: 'lon', value: 'lon' },
                { text: 'alt (km)', value: 'alt' },
                { text: 'gps_numsats', value: 'gps_numsats' }
            ],
        }
    },
    methods: {
        parseAndSetValues(payload) {
            const messageOBJ = JSON.parse(payload)
            // both frame types -
            this.info[0].lat = (messageOBJ.tracker.gps['gps_lat']).toFixed(1)  + '°'
            this.info[0].lon = (messageOBJ.tracker.gps['gps_lon']).toFixed(1)   + '°'
            this.info[0].alt = (messageOBJ.tracker.gps['gps_alt'] / 1000).toFixed(2)
            this.info[0].gps_numsats = messageOBJ.tracker.gps['gps_numsats']
        }
    }
}
</script>

<style>
    .card-styles {
        padding: 0.1em;
        width: 11em;
    }
    #position-title{
        font-size: 1em;
        padding: 0 0.5em;
        color: rgba(0, 0, 0, 0.6);
        font-weight: bolder;
    }
    .wrap{
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: center;
        font-size: 0.8em;
        margin: 0.75em 0;
    }
    .spacing {
        margin: 0 0.5em;
    }
    td {
        text-align: center !important;
    }
</style>