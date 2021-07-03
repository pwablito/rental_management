<template>
  <div class="rentalmanagement">
    <h1>{{ msg }}</h1>
    <div class="centered content">
      <LoginRegister v-if="!this.is_logged_in" @register_user="set_user" />
    </div>
  </div>
</template>

<script>

import LoginRegister from './LoginRegister.vue';

export default {
  name: 'RentalManagement',
  components: {
    LoginRegister
  },
  props: {
    msg: String
  },
  data() {
    return {
      user: null
    }
  },
  computed: {
    is_logged_in() {
      return this.user !== null
    }
  },
  methods: {
    set_user(payload) {
      this.user = payload.user
    }
  }
}
</script>

<style scoped>
.centered {
  text-align: center;
  justify-content: center;
}

.content {
  max-width: 800px;
}
</style>
