<template>
  <div id="browseview">
    <b-tabs content-class="mt-3" align="center" pills>
      <b-tab title="List" active>
        <div id="loading_div" class="centered" v-if="this.loading">Loading</div>
        <div v-else>
          <p>Listings:</p>
          <p v-if="this.listings.length === 0">None found</p>
          <ul v-else>
            <ListingView
              v-for="listing in this.listings"
              :key="listing.id"
              :listing="listing"
            />
          </ul>
          <p class="red" v-if="this.error_message !== ''">
            {{ this.error_message }}
          </p>
          <button class="btn btn-primary" @click="this.get_listings">
            Reload
          </button>
        </div>
      </b-tab>
      <b-tab title="Map">
        <MapListingsView :listings="listings" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";
import ListingView from "./ListingView.vue";
import MapListingsView from "./MapListingsView.vue";

export default {
  name: "BrowseView",
  props: {
    token: String,
  },
  components: {
    ListingView,
    MapListingsView
  },
  data() {
    return {
      listings: [],
      loading: false,
      error_message: "",
    };
  },
  created() {
    this.get_listings();
  },
  methods: {
    get_listings() {
      this.loading = true;
      this.error_message = null;
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
        })
        .then(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style>
.red {
  color: red;
}
.centered {
  text-align: center;
}
</style>
