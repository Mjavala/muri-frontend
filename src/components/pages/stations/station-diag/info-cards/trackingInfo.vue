<template>
    <div>
        <v-card id="tracking-card" flat>
            <v-card-title id="tracking-title">Ground station info</v-card-title>
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
                range: 105,
                Az: 39,
                req_Az: 17000,
                req_El: 50,
                curr_Az: 100,
                elv: 5000,
                last_req_mode: 'WAITING',
                last_req_mode_time: 'WAITING',
                last_man_az: 0,
                last_man_elv: 0,
            }],
            headers: [
                { text: 'range', value: 'range' },
                { text: 'Az', value: 'Az' },
                { text: 'req_Az', value: 'req_Az' },
                { text: 'req_El', value: 'req_El' },
                { text: 'curr_Az', value: 'curr_Az' },
                { text: 'elv', value: 'elv' },
                { text: 'last_req_mode', value: 'last_req_mode' },
                { text: 'last_req_mode_time', value: 'last_req_mode_time' },
                { text: 'last_man_az', value: 'last_man_az' },
                { text: 'last_man_elv', value: 'last_man_elv' }
            ],
        }
    },
    methods: {
        parseAndSetValues(payload) {
            const messageOBJ = JSON.parse(payload)
            // both frame types -
            this.info[0].range = (messageOBJ.tracker.track['last_range']).toFixed(1)
            this.info[0].Az = messageOBJ.tracker.ant['azm']
            this.info[0].req_Az = messageOBJ.tracker.ant['req_azm']
            this.info[0].req_El = messageOBJ.tracker.ant['req_elv']
            // is curr Az curr?
            this.info[0].curr_Az = messageOBJ.tracker.ant['curr']
            this.info[0].elv = messageOBJ.tracker.ant['elv']
            this.info[0].last_req_mode = messageOBJ.tracker.rotator['last_req_mode']
            this.info[0].last_req_mode_time = messageOBJ.tracker.rotator['last_req_mode_time']
            this.info[0].last_man_az = messageOBJ.tracker.rotator['last_man_az']
            this.info[0].last_man_elv = messageOBJ.tracker.rotator['last_man_elv']
        }
    }
}
</script>

<style scoped>
    .card-styles {
        padding: 0.1em;
        width: 17.5em;
    }
    .wrap{
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: center;
        font-size: 0.8em;
        margin: 0.75em 0;
    }
    #tracking-title {
        font-size: 1em;
        padding: 0 0.5em;
        color: rgba(0, 0, 0, 0.6);
        font-weight: bolder;
    }
    .balloon-info {
        font-size: 1.1em;
        padding-left: 0.5em;
        width: 50%;
        border-bottom: 1px black solid;
    }
    .balloon-sub-info {
        font-size: 1em;
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
        margin-right: 0;
    }
    #tracking-card{
        max-width: 95% !important;
    }
</style>