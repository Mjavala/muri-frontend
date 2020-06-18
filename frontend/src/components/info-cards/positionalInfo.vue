<template>
    <div>
        <v-card id="positional-card" flat>
            <v-card-title id="pos-title">Station Positional Info</v-card-title>
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
            this.info[0].lon = (messageOBJ.tracker.gps['gps_lon']).toFixed(1)  + '°'
            this.info[0].alt = (messageOBJ.tracker.gps['gps_alt'] / 1000).toFixed(2)
            this.info[0].gps_numsats = messageOBJ.tracker.gps['gps_numsats']
        }
    }
}
</script>

<style scoped>
    .card-styles {
        padding: 0.1em;
        width: 11em;
    }
    .wrap{
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: center;
        font-size: 0.8em;
        margin: 0.75em 0;
    }
    .balloon-info {
        font-size: 1.1em;
        padding-left: 0.5em;
        width: 75%;
        border-bottom: 1px black solid;
    }
    .inline {
        background-color: white;
        display: inline;
        border: 1px solid grey;
        border-radius: 2.5px;
        padding: 0.1em;
    }
    .spacing {
        margin: 0 0.5em;
    }
    #pos-title{
        font-size: 0.8em;
        padding: 0 0.5em;
        color: rgba(0, 0, 0, 0.6);
        font-weight: bolder;
    }
</style>