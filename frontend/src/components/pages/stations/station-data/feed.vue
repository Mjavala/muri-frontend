<template>
    <v-container id="feed" />
</template>

<script>
export default {
    data(){
        return {
            messageMain: '',
        }
    },
    props: [
        'balloonInfoMessage', 'stationTrackingInfoMessage'
    ],
    watch: {
        balloonInfoMessage(newVal){
            this.messageMain = newVal
            this.addToFeed()
        },
        stationTrackingInfoMessage (newVal){
            this.messageMain = newVal
            this.addToFeedStat()
        }
    },
    methods: {
        addToFeed(){
            let feed = document.getElementById('feed')
            const message = JSON.parse(this.messageMain)
            feed.innerHTML = 'muri/raw' + ' ' + JSON.stringify(message, undefined, '\t') ;
        },
        addToFeedStat () {
            let feed = document.getElementById('feed');
            const message = JSON.parse(this.messageMain)
            feed.innerHTML = 'muri/stat' + ' ' + JSON.stringify(message, undefined, '\t')
        }
    }
}
</script>

<style scoped>
    #feed{
        position: fixed;
        top: 8%;
        right: 0;
        width: 20vw;
        height: 100vh;
        border: solid grey;
        border-radius: 5px;
        border-width: 1px;
        z-index: 10;
        background-color: white;
        overflow-y: scroll;
    }
</style>>
