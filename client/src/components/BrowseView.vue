<template>
  <div id="browseview">
      Listings:
      <ul>
          <li v-for="listing in this.listings" :key="listing">
              {{listing}}
          </li>
      </ul>
    <p class="red" v-if="this.error_message !== ''">{{this.error_message}}</p>
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
</style>
