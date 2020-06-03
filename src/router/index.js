import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/homePage.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/muri/historical',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../components/historical.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
