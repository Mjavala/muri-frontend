<template>
  <div>
    <v-container
        id="feed"
        style="max-height: 200px"
    >
    </v-container>
  </div>
</template>

<script>
export default {
    data(){
        return {
            messageMain: '',
        }
    },
    props: [
        'message'
    ],
    watch: {
        message(newVal){
            this.messageMain = newVal
            this.addToFeed()
        }
    },
    methods: {
        addToFeed(){
            let feed = document.getElementById('feed');
            feed.innerHTML = this.messageMain ;
        }
    }
}
</script>

<style scoped>
    #feed{
        border: solid black;
        border-width: 1px;
        overflow-x: scroll;
    }
</style>>
