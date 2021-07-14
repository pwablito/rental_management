<template>
  <div id="maplistingsview">
    <GmapMap
      :center="{ lat: 0, lng: 0 }"
      :zoom="2"
      style="width:100%;  height: 600px;"
    >
      <GmapMarker
        v-for="listing in listings"
        :key="listing.id"
        :position="{ lat: listing.latitude, lng: listing.longitude }"
        :title="listing.name"
        :clickable="true"
        @click="show_listing_modal(listing)"
      />
    </GmapMap>
    <b-modal
      title="Listing"
      ok-only
      v-for="listing in listings"
      :key="listing.id"
      v-model="show_modal"
    >
      <div v-if="modal_listing">
        <p>Name: {{ modal_listing.name }}</p>
        <p>Description: {{ modal_listing.description }}</p>
        <p>Floor Area: {{ modal_listing.floor_area }} sq. ft.</p>
        <p>Price: ${{ modal_listing.price }}/month</p>
        <p>Beds: {{ modal_listing.rooms }}</p>
        <p>Baths: {{ modal_listing.bathrooms }}</p>
        <p>Realtor: {{ modal_listing.realtor }}</p>
        <p>Created: {{ date_format(modal_listing.created_on) }}</p>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "MapListingsView",
  data() {
    return {
      show_modal: false,
      modal_listing: null,
    };
  },
  props: {
    listings: [],
  },
  methods: {
    show_listing_modal(listing) {
      this.modal_listing = listing;
      this.show_modal = true;
    },
    date_format(date) {
      return new Date(date).toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
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
