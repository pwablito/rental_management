<template>
  <div id="editlistingview">
    <div>
        Edit Listing:
        {{listing}}
        <button @click="reset" class="btn btn-default">Cancel</button>
        <button @click="update" class="btn btn-success">Done</button>
        <button @click="delete_listing" class="btn btn-danger">Delete</button>
    </div>
    <p class="red centered" v-if="this.error_message">{{this.error_message}}</p>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: "EditListingView",
  data() {
    return {
      editing: false,
      edit_listing: {},
      loading: false,
      error_message: null,
    };
  },
  props: {
      listing: Object,
  },
  methods: {
      reset() {
          this.edit_listing = this.listing;
      },
      update() {
          this.loading = true;
          this.error_message = null;
          axios.post(
              "/api/update_listing", {
                  listing: this.edit_listing,
              }
          ).then((response) => {
              if (response.data.success) {
                  this.listing = this.edit_listing;
              } else {
                  this.error_message = this.data.message;
              }
          }).error(() => {
              this.error_message = "Something went wrong";
          }).then(() => {
              this.loading = false;
          })
      },
      delete_listing() {
          this.loading = true;
          this.error_message = null;
          axios.post(
              "/api/delete_listing", {
                  listing_id: this.listing.id,
              }
          ).then((response) => {
              if (response.data.success) {
                  alert("Success");
                  // Maybe send a message up one level to destroy the listing?
              } else {
                  this.error_message = this.data.message;
              }
          }).error(() => {
              this.error_message = "Something went wrong";
          }).then(() => {
              this.loading = false;
          })
      }
  },
  created() {
      this.edit_listing = this.listing;
  }
};
</script>

<style>
.red {
    color: red;
}
.centered {
    text-align: center;
}</style>
