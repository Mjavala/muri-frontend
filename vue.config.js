module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  configureWebpack: {
    externals: {
      Vue: "vue"
    }
  }
}