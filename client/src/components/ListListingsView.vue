<template>
  <div id="listlistingsview">
    <div class="row left-aligned">
      <div class="col-1 item">Name</div>
      <div class="col-1 item">Realtor</div>
      <div class="col-3 item">Description</div>
      <div class="col-1 item">Floor Area</div>
      <div class="col-1 item">Price</div>
      <div class="col-2 item">Bed/Bath</div>
      <div class="col-2 item">Created</div>
      <div class="col-1 item">Lat/Lon</div>
    </div>
    <hr />
    <div
      v-for="listing in this.listings"
      :key="listing.id"
      class="left-aligned"
    >
      <ListingView :listing="listing" />
      <hr>
    </div>
  </div>
</template>

<script>
import ListingView from "./ListingView.vue";

export default {
  name: "ListListingsView",
  props: {
    listings: [],
  },
  components: {
    ListingView,
  },
};
</script>

<style>
.centered {
  text-align: center;
}
.left-aligned {
  text-align: left;
}
.red {
  color: red;
}
</style>
