<template>
    <div>
        <v-card id="balloon-card" flat>
            <div id="balloon-title">Balloon Info - tracking [{{this.current_balloon}}]</div>
            <v-data-table disable-sort dense hide-default-footer :headers="headers" :items="info" item-key="name"></v-data-table>
        </v-card>
    </div>
</template>

<script>
export default {
    props: ['balloonInfoMessage', 'balloonToTrack'],
    watch: {
        balloonInfoMessage (newVal) {
            this.payload = newVal
            if (this.current_balloon !== ''){
                this.parseAndSetValues(this.payload)            
            }
        },
        balloonToTrack (newVal) {
            this.current_balloon = newVal
        }
    },
    data () {
        return {
            payload: '',
            current_balloon: '',
            info: [{
                lat: '     ',
                lon: 25.0,
                alt: 51,
                velx: 4.9,
                vely: 85,
                velz: 59,
                wind: 20,
                temp: 201,
                RMS_Hor_Vel: 29230,
                RMS_Ver_Vel: 0,
                interval_index: 1022,
                epoch_index: 100,
                vent: 102
            }],
            headers: [
                { text: 'lat', value: 'lat',},
                { text: 'lon', value: 'lon' },
                { text: 'alt (km)', value: 'alt' },
                { text: 'vx (m/s)', value: 'velx' },
                { text: 'vy (m/s)', value: 'vely' },
                { text: 'vz (m/s)', value: 'velz' },
                { text: 'wind', value: 'wind' },
                { text: 'temp (k)', value: 'temp' },
                { text: 'RMS_HVel', value: 'RMS_Hor_Vel' },
                { text: 'RMS_VVel', value: 'RMS_Ver_Vel'},
                { text: 'interval_index', value: 'interval_index' },
                { text: 'epoch_index', value: 'epoch_index' },
                { text: 'vent', value: 'vent' },
            ],
        }
    },
    methods: {
        parseAndSetValues(payload) {
            const messageOBJ = JSON.parse(payload)

            if (messageOBJ.data['ADDR_FROM'] === this.current_balloon) {
                // both frame types -
                this.info[0].lat = (messageOBJ.data.frame_data['gps_lat'] / 10000000).toFixed(1)  + '°'
                this.info[0].lon = (messageOBJ.data.frame_data['gps_lon'] / 10000000).toFixed(1) + '°'
                this.info[0].alt = (messageOBJ.data.frame_data['gps_alt'] / 1000000).toFixed(1)
                this.info[0].epoch_index = messageOBJ.data.frame_data['epoch index']
                
                // 0xd2a8 only
                // asuming gps_veln (n = north = y), gps_vele (e = east = x), gps_vel_d(d = down = -z)
                if (messageOBJ.data['FRAME_TYPE'] === '0xd2a8') {
                    this.info[0].velx = messageOBJ.data.frame_data['gps_veln']
                    this.info[0].vely = messageOBJ.data.frame_data['gps_vele']
                    this.info[0].velz = messageOBJ.data.frame_data['gps_vel_d']
                    // temp Ta1 (amb)
                    this.info[0].temp = messageOBJ.data.frame_data['temp Ta1 (amb)']
                    // what's wind? what's vent?
                    this.info[0].RMS_Hor_Vel = messageOBJ.data.frame_data['RMS Hor Vel']
                    this.info[0].RMS_Ver_Vel = messageOBJ.data.frame_data['RMS Ver Vel']
                }
                // 0xc109 only
                if (messageOBJ.data['FRAME_TYPE'] === '0xc109') {
                    this.info[0].interval_index = messageOBJ.data.frame_data['interval index']
                }
            }
        }
    }
}
</script>

<style>
    .card-styles {
        padding: 0.1em;
        width: 16em;
    }
    td {
        text-align: center !important;
    }
    .wrap{
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: center;
        font-size: 0.8em;
        margin: 0.75em 0;
    }
    #balloon-title{
        font-size: 0.8em;
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
    .v-data-table{
        max-width: 100% !important;
    }
    .v-data-table td, .v-data-table th {
        padding: 0 8px !important;
    }
    #balloon-card{
        max-width: 95% !important;
    }
    .v-data-table th{
        font-size: 0.7rem !important;
    }
    .v-data-table td{
        font-size: 0.7rem !important
    }
</style>