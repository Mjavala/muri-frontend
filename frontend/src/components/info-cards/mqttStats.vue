<template>
    <div>
        <v-card id="mqtt-card">
            <v-card-title id="mqtt-title">Mqtt stat info</v-card-title>
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
                Qin: 105,
                Qout: 39,
                period: 170,
                in: 10,
                out: 20,
            }],
            headers: [
                { text: 'Qin', value: 'Qin' },
                { text: 'Qout', value: 'Qout' },
                { text: 'period', value: 'period' },
                { text: 'in', value: 'in' },
                { text: 'out', value: 'out' },
            ],
        }
    },
    methods: {
        parseAndSetValues(payload) {
            const messageOBJ = JSON.parse(payload)
            this.info[0].Qin = (messageOBJ.mqtt['mqtt_qIn'])
            this.info[0].Qout = messageOBJ.mqtt['mqtt_qOut']
            this.info[0].period = (messageOBJ.mqtt['period']).toFixed(2)
            this.info[0].in = messageOBJ.mqtt['mqtt_in']
            this.info[0].out = messageOBJ.mqtt['mqtt_out']
        }
    }
}
</script>

<style scoped>
    .card-styles {
        padding: 0.1em;
        width: 12em;
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
    #mqtt-title{
        font-size: 1em;
        padding: 0 0.5em;
        color: rgba(0, 0, 0, 0.6);
        font-weight: bolder;
    }
    .inline {
        background-color: white;
        display: inline;
        border: 1px solid grey;
        border-radius: 2.5px;
        padding: 0.1em;
    }
    #mqtt-card {
        position: absolute;
        left: 56.5%;
        top: 87.6%;
    }
</style>