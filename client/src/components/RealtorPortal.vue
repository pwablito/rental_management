<template>
  <div id="realtorportal">
    <h2 class="centered">Realtor Portal</h2>
    <div>
  <b-tabs content-class="mt-3" align="center" pills>
    <b-tab title="Profile" active><ProfileView :token="this.token" :user="this.user" @logout="logout" /></b-tab>
    <b-tab title="Browse"><BrowseView :token="this.token"/></b-tab>
    <b-tab title="Create"><CreateListingView :token="this.token"/></b-tab>
    <b-tab title="Edit"><EditListingsView :token="this.token"/></b-tab>
  </b-tabs>
</div>
  </div>
</template>

<script>
import ProfileView from './ProfileView.vue';
import BrowseView from './BrowseView.vue';
import CreateListingView from './CreateListingView.vue';
import EditListingsView from './EditListingsView.vue';

export default {
  name: 'RealtorPortal',
  props: {
    token: String,
    user: Object,
  },
  components: {
    ProfileView,
    BrowseView,
    CreateListingView,
    EditListingsView,
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
