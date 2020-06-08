<template>    
    <v-app-bar
        app
        dark
        id="nav"
    >
      <v-img id="iriss-logo" max-height="100" max-width="225" src="../../../../assets/iriss_logo.png" />
      <v-spacer />
      <v-btn light small>
          <router-link to="/">Home</router-link>
      </v-btn>
    </v-app-bar>
</template>

<style>
  #nav{
    position: absolute;
    z-index: 1000;
    background: #667db6;  /* fallback for old browsers */
    background: -webkit-linear-gradient(to right, #667db6, #0082c8, #0082c8, #667db6) !important;  /* Chrome 10-25, Safari 5.1-6 */
    background: linear-gradient(to right, #667db6, #0082c8, #0082c8, #667db6) !important;
  }
  a {
    color: inherit;
    text-decoration: none;
  }
  .active {
    background-color: #76FF03 !important;
  }
</style>