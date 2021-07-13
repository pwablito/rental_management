<template>
  <div id="adminportal">
    <h2 class="centered">Admin Portal</h2>
    <div>
  <b-tabs content-class="mt-3" align="center" pills>
    <b-tab title="Profile" active><ProfileView :token="this.token" :user="this.user" @logout="logout" /></b-tab>
    <b-tab title="Browse"><BrowseView :token="this.token"/></b-tab>
      <b-tab title="Create">
        <b-tabs content-class="mt-3" align="center" pills>
          <b-tab title="Listing">
            <CreateListingView :token="this.token"/>
          </b-tab>
          <b-tab title="User">
            <CreateUserView :token="this.token"/>
          </b-tab>
        </b-tabs>
    </b-tab>
    <b-tab title="Edit">
        <b-tabs content-class="mt-3" align="center" pills>
          <b-tab title="Listings">
            <EditListingsView :token="this.token"/>
          </b-tab>
          <b-tab title="Users">
            <EditUsersView :token="this.token"/>
          </b-tab>
        </b-tabs>
    </b-tab>
  </b-tabs>
</div>
  </div>
</template>

<script>
import ProfileView from './ProfileView.vue';
import BrowseView from './BrowseView.vue';
import CreateListingView from './CreateListingView.vue';
import EditListingsView from './EditListingsView.vue';
import EditUsersView from './EditUsersView.vue';
import CreateUserView from './CreateUserView.vue';

export default {
  name: 'AdminPortal',
  props: {
    token: String,
    user: Object,
  },
  components: {
    ProfileView,
    BrowseView,
    CreateListingView,
    EditListingsView,
    EditUsersView,
    CreateUserView,
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
