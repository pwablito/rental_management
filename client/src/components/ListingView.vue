<template>
  <div id="listingview">
    <div>
        <p>Name: {{this.listing.name}}</p>
        <p>Description: {{this.listing.description}}</p>
        <p>Floor Area: {{this.listing.floor_area}}</p>
        <p>Price: {{this.listing.price}}</p>
        <p>Rooms: {{this.listing.rooms}}</p>
        <p>Bathrooms: {{this.listing.bathrooms}}</p>
        <p>Latitude: {{this.listing.latitude}}</p>
        <p>Longitude: {{this.listing.longitude}}</p>
        <p>Created on: {{this.created_on_date}}</p>

    </div>
    <p class="red centered" v-if="this.error_message">{{this.error_message}}</p>
  </div>
</template>
<script>

export default {
  name: "ListingView",
  data() {
    return {
      loading: false,
    };
  },
  props: {
      listing: Object,
  },
  computed: {
      created_on_date() {
          return Date.parse(this.listing.created_on)
      }
  }
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
