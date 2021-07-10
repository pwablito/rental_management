<template>
  <div id="editlistings">
    <div v-for="listing in this.listings" :key="listing.id">
      <EditListingView :listing="listing" />
    </div>

    <button class="btn btn-primary" @click="this.get_listings">
      Reload
    </button>
  </div>
</template>

<script>
import axios from "axios";
import EditListingView from "./EditListingView.vue";

export default {
  name: "EditListingsView",
  props: {
    token: String,
  },
  components: {
    EditListingView,
  },
  data() {
    return {
      listings: [],
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
.centered {
  text-align: center;
}
.red {
  color: red;
}
</style>
