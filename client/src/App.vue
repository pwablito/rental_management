<template>
  <div id="app">
    <RentalManagement />
  </div>
</template>

<script>
import RentalManagement from './components/RentalManagement.vue'

export default {
  name: 'App',
  components: {
    RentalManagement
  }
}
</script>

<style>
#app {
  text-align: center;
  margin-left: 20%;
  margin-right: 20%;
}
</style>
