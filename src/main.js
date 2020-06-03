import { Icon }  from 'leaflet'
import 'leaflet/dist/leaflet.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

import { ApolloClient } from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import VueApollo from 'vue-apollo';

Vue.use(VueApollo);

const getHeaders = () => {

  let headers = {};

     headers = {
     'content-type': `application/json`,
     'x-hasura-access-key': 'mylongsecretkey'
     }
   console.log(headers)

   return headers;

 };
// Create a new HttpLink to connect to your GraphQL API.
// According to the Apollo docs, this should be an absolute URI.
 // Create an http link:

 const link = new HttpLink({

  uri: 'http://64.227.104.52:8080/v1alpha1/graphql',

  fetch,

  headers: getHeaders()

});
console.log(link)
const client = new ApolloClient({

  link: link,

  cache: new InMemoryCache({

    addTypename: true

  })

});

const apolloProvider = new VueApollo({

  defaultClient: client,

})

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  apolloProvider,
  render: h => h(App)
}).$mount('#app')
