<template>
  <div id="browseview">
    <div id="loading_div" class="centered" v-if="this.loading">Loading</div>
    <div v-else>
      <p>Listings:</p>
      <ul>
        <p v-if="this.listings.length === 0">None found</p>
        <li v-for="listing in this.listings" :key="listing.id">
            {{listing}}
        </li>
      </ul>
      <p class="red" v-if="this.error_message !== ''">{{this.error_message}}</p>
      <button class="btn btn-primary" @click="this.get_listings">Reload</button>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'BrowseView',
  props: {
      token: String,
  },
  data() {
      return {
          listings: [],
          loading: false,
          error_message: "",
      }
  },
  created() {
      this.get_listings();
  },
  methods: {
      get_listings() {
          this.loading = true;
          axios
          .post("/api/get_listings", {
            token: this.token,
          })
          .then((response) => {
            if (response.data.success) {
                this.listings = response.data.listings;
            } else {
              this.error_message = response.data.message;
            }
          })
          .catch(() => {
            this.error_message = "Something went wrong";
          }).then(() => {
              this.loading = false;
          })
      }
  }
}
</script>

<style>
.red {
    color: red;
}
.centered {
  text-align: center;
}
</style>
