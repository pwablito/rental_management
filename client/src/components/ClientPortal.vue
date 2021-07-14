<template>
  <div id="clientportal">
    <h2 class="centered">Client Portal</h2>
    <div>
  <b-tabs content-class="mt-3" align="center" pills>
    <b-tab title="Profile"><ProfileView :token="this.token" :user="this.user" @logout="logout" /></b-tab>
    <b-tab title="Browse" active><BrowseView :token="this.token"/></b-tab>
  </b-tabs>
</div>
  </div>
</template>

<script>
import ProfileView from './ProfileView.vue';
import BrowseView from './BrowseView.vue';

export default {
  name: 'ClientPortal',
  props: {
    token: String,
    user: Object,
  },
  components: {
    ProfileView,
    BrowseView,
  },
  methods: {
    logout() {
      this.$emit("logout");
    }
  }
}
</script>

<style>
.centered {
  text-align: center;
}
</style>
