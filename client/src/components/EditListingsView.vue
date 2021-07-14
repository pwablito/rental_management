<template>
  <div id="editlistings" class="centered">
    <div id="filters" class="centered">

      <div class="row">
        <div class="col-6">
          <div class="input-group input-group-sm ">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroup-sizing-sm">Min Floor Area</span>
            </div>
            <input
              type="number"
              class="form-control"
              aria-label="Min Floor Area"
              aria-describedby="inputGroup-sizing-sm"
              v-model="filters.floor_area_min"
            />
          </div>
        </div>
        <div class="col-6">
          <div class="input-group input-group-sm ">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroup-sizing-sm">Max Floor Area</span>
            </div>
            <input
              type="number"
              class="form-control"
              aria-label="Max Floor Area"
              aria-describedby="inputGroup-sizing-sm"
              v-model="filters.floor_area_max"
            />
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-6">
          <div class="input-group input-group-sm ">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroup-sizing-sm">Min Price</span>
            </div>
            <input
              type="number"
              class="form-control"
              aria-label="Min Price"
              aria-describedby="inputGroup-sizing-sm"
              v-model="filters.price_min"
            />
          </div>
        </div>
        <div class="col-6">
          <div class="input-group input-group-sm ">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroup-sizing-sm">Max Price</span>
            </div>
            <input
              type="number"
              class="form-control"
              aria-label="Max Price"
              aria-describedby="inputGroup-sizing-sm"
              v-model="filters.price_max"
            />
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-6">
          <div class="input-group input-group-sm ">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroup-sizing-sm">Min Rooms</span>
            </div>
            <input
              type="number"
              class="form-control"
              aria-label="Min Rooms"
              aria-describedby="inputGroup-sizing-sm"
              v-model="filters.bed_min"
            />
          </div>
        </div>
        <div class="col-6">
          <div class="input-group input-group-sm ">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroup-sizing-sm">Max Rooms</span>
            </div>
            <input
              type="number"
              class="form-control"
              aria-label="Max Rooms"
              aria-describedby="inputGroup-sizing-sm"
              v-model="filters.bed_max"
            />
          </div>
        </div>
      </div>
    </div>

    <br><br>

    <div class="row">
      <div class="col-1 item">Name</div>
      <div class="col-2 item">Description</div>
      <div class="col-1 item">Floor Area</div>
      <div class="col-1 item">Price</div>
      <div class="col-1 item">Bed/Bath</div>
      <div class="col-2 item">Created</div>
      <div class="col-1 item">Lat/Lon</div>
      <div class="col-1 item">Listed</div>
      <div class="col-2 item">Edit/Delete</div>
    </div>
    <hr />
    <div v-for="listing in this.listings" :key="listing.id">
      <div v-if="satisfies_filters(listing)">
        <EditListingView
          :listing="listing"
          :token="token"
          @update_listings="get_listings"
        />
        <hr />
      </div>
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
      filters: {
        floor_area_min: null,
        floor_area_max: null,
        price_min: null,
        price_max: null,
        bed_min: null,
        bed_max: null,
      },
    };
  },
  created() {
    this.get_listings();
  },
  methods: {
    satisfies_filters(listing) {
      if (listing === null) {
        return false;
      }
      if (this.filters.floor_area_min !== null) {
        if (listing.floor_area < this.filters.floor_area_min) {
          return false;
        }
      }
      if (this.filters.floor_area_max !== null) {
        if (listing.floor_area > this.filters.floor_area_max) {
          return false;
        }
      }
      if (this.filters.price_min !== null) {
        if (listing.price < this.filters.price_min) {
          return false;
        }
      }
      if (this.filters.price_max !== null) {
        if (listing.price > this.filters.price_max) {
          return false;
        }
      }
      if (this.filters.bed_min !== null) {
        if (listing.rooms < this.filters.bed_min) {
          return false;
        }
      }
      if (this.filters.bed_max !== null) {
        if (listing.rooms > this.filters.bed_max) {
          return false;
        }
      }
      return true;
    },
    get_listings() {
      this.loading = true;
      this.error_message = null;
      this.listings = [];
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
#editlistingsview {
  font-size: 11px;
  font-weight: bold;
}
.item {
  padding-left: 0px !important;
  padding-right: 0px !important;
}
.centered {
  text-align: center;
}
.red {
  color: red;
}
</style>
