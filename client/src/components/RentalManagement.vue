<template>
  <div class="rentalmanagement left-aligned">
    <div>
      <LoginRegister v-if="!this.is_logged_in" @set_user="set_user" @set_token="set_token" />
      <div v-else>
        <ClientPortal v-if="this.is_client" :user="this.user" :token="this.token" @logout="logout" />
        <RealtorPortal v-if="this.is_realtor" :user="this.user" :token="this.token" @logout="logout" />
        <AdminPortal v-if="this.is_admin" :user="this.user" :token="this.token" @logout="logout" />
      </div>
    </div>
  </div>
</template>

<script>

import LoginRegister from './LoginRegister.vue';
import ClientPortal from './ClientPortal.vue'
import RealtorPortal from './RealtorPortal.vue'
import AdminPortal from './AdminPortal.vue'

export default {
  name: 'RentalManagement',
  components: {
    LoginRegister,
    ClientPortal,
    RealtorPortal,
    AdminPortal,
  },
  data() {
    return {
      user: null,
      token: null,
    }
  },
  computed: {
    is_logged_in() {
      return this.user !== null;
    },
    is_client() {
      if (this.user) {
        return this.user.type === "client";
      }
      return false;
    },
    is_realtor() {
      if (this.user) {
        return this.user.type === "realtor";
      }
      return false;
    },
    is_admin() {
      if (this.user) {
        return this.user.type === "admin";
      }
      return false;
    },
  },
  methods: {
    set_user(payload) {
      this.user = payload.user;
    },
    set_token(payload) {
      this.token = payload.token;
    },
    logout() {
      this.user = null;
      this.token = null;
    }
  }
}
</script>

<style scoped>
.left-aligned {
  text-align: left;
}
</style>
