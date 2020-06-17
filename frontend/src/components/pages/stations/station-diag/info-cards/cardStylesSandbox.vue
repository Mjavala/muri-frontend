<template>
    <div>
        <v-card  class="card-styles" color="#E0E0E0" >
            <v-list-item-subtitle class="balloon-info">Balloon info</v-list-item-subtitle>
            <div class="wrap">
                <div class="spacing">
                    velX: <div class="inline"> {{this.velx}} </div>
                </div>
                <div class="spacing">
                    velY: <div class="inline"> {{this.vely}} </div>
                </div>
                <div class="spacing">
                    velZ: <div class="inline"> {{this.velz}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    Wind: <div class="inline"> {{this.wind}} </div>
                </div>
                <div class="spacing">
                    Temp: <div class="inline"> {{this.temp}} </div>
                </div>
                <div class="spacing">
                    RMS: <div class="inline"> {{this.rms}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    last record index: <div class="inline"> {{this.lri}} </div>
                </div>
                <div class="spacing">
                    last epoch index: <div class="inline"> {{this.lei}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    lat: <div class="inline"> {{this.lat}} </div>
                </div>
                <div class="spacing">
                    lon: <div class="inline"> {{this.lon}} </div>
                </div>
                <div class="spacing">
                    alt: <div class="inline"> {{this.alt}} </div>
                </div>
                <div class="spacing">
                    vent: <div class="inline"> {{this.vent}} </div>
                </div>
            </div>
        </v-card>
        <v-card  class="card-styles" color="#E0E0E0" >
            <v-list-item-subtitle class="balloon-info">MQTT stats</v-list-item-subtitle>
            <div class="wrap">
                <div class="spacing">
                    Qin: <div class="inline"> {{this.Qin}} </div>
                </div>
                <div class="spacing">
                    Qout: <div class="inline"> {{this.Qout}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    period: <div class="inline"> {{this.period}} </div>
                </div>
                <div class="spacing">
                    in: <div class="inline"> {{this.in}} </div>
                </div>
                <div class="spacing">
                    out: <div class="inline"> {{this.out}} </div>
                </div>
            </div>
        </v-card>
        <v-card  class="card-styles" color="#E0E0E0" >
            <v-list-item-subtitle class="balloon-info">Tracking info</v-list-item-subtitle>
            <div class="wrap">
                <div class="spacing">
                    Range: <div class="inline"> {{this.range}} </div>
                </div>
                <div class="spacing">
                    Azimuth: <div class="inline"> {{this.Azimuth}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    Req Azimuth: <div class="inline"> {{this.rAzimuth}} </div>
                </div>
                <div class="spacing">
                    Req Elevation: <div class="inline"> {{this.rElevation}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    Current Azimuth: <div class="inline"> {{this.cAzimuth}} </div>
                </div>
                <div class="spacing">
                    Current Elevation: <div class="inline"> {{this.cElevation}} </div>
                </div>
            </div>
            <v-list-item-subtitle class="balloon-sub-info">Rotator State Info</v-list-item-subtitle>
            <div class="wrap">
                <div class="spacing">
                    Last Man Az: <div class="inline"> {{this.lmaz}} </div>
                </div>
                <div class="spacing">
                    Last Man Elv: <div class="inline"> {{this.lmelv}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    Mode: <div class="inline"> {{this.mode}} </div>
                </div>
                <div class="spacing">
                    Last Req Mode: <div class="inline"> {{this.lrm}} </div>
                </div>
            </div>
        </v-card>
        <v-card  class="card-styles" color="#E0E0E0" >
            <v-list-item-subtitle class="balloon-info">Positional info</v-list-item-subtitle>
            <div class="wrap">
                <div class="spacing">
                    lat: <div class="inline"> {{this.lat}} </div>
                </div>
                <div class="spacing">
                    lon: <div class="inline"> {{this.lon}} </div>
                </div>
            </div>
            <div class="wrap">
                <div class="spacing">
                    alt: <div class="inline"> {{this.alt}} </div>
                </div>
                <div class="spacing">
                    num sats: <div class="inline"> {{this.ns}} </div>
                </div>
            </div>
        </v-card>
    </div>
</template>

<script>
export default {
    data () {
        return {
            lat: 105,
            lon: 39,
            alt: 17000,
            velx: 50,
            vely: 100,
            velz: 120,
            wind: 5000,
            temp: 200,
            rms: 50,
            lri: 2,
            lei: 10,
            vent: 100,
            range: 105,
            Azimuth: 39,
            rAzimuth: 17000,
            rElevation: 50,
            cAzimuth: 100,
            rotator: 120,
            cElevation: 5000,
            mode: 'WAITING',
            lrm: 'WAITING',
            lmaz: 0,
            lmelv: 0,
            Qin: 105,
            Qout: 39,
            period: 170,
            in: 10,
            out: 20,
            lat: 105,
            lon: 39,
            alt: 17000,
            ns: 1000,
        }
    }
}
</script>