<template>
    <div>
        <navbar />
        <div id="diag-wrap">
            Coming Soon...
        </div>      
    </div>
</template>

<script>
import navbar from './navbar'
export default {
    components: {
        navbar
    }
}
</script>

<style scoped>
    #diag-wrap {
        height: 100vh;
        font-size: 5em;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>