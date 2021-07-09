<template>
  <div id="listview">
    <div v-if="editing">
        Edit
        {{listing}}
        <button @click="cancel_editing">Cancel</button>
        <button @click="update">Done</button>
    </div>
    <div v-else>
        <p>Name: {{listing.name}}</p>
        <p>Description: {{listing.description}}</p>
        <p>Floor Area: {{listing.floor_area}}</p>
        <p>Bedrooms: {{listing.bedrooms}}</p>
        <p>Bathrooms: {{listing.bathrooms}}</p>

        <button @click="edit">Edit</button>

    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: "ListView",
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
      edit() {
          this.editing = true;
      },
      cancel_editing() {
          this.editing = false;
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
      }
  },
  created() {
      this.edit_listing = this.listing;
  }
};
</script>

<style></style>
