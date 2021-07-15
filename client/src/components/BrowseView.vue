<template>
  <div id="browseview" class="centered">
    <b-tabs content-class="mt-3" align="center" pills>
      <div id="filters" class="centered">
        <div class="row">
          <div class="col-6">
            <div class="input-group input-group-sm ">
              <div class="input-group-prepend">
                <span class="input-group-text" id="inputGroup-sizing-sm"
                  >Min Floor Area</span
                >
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
                <span class="input-group-text" id="inputGroup-sizing-sm"
                  >Max Floor Area</span
                >
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
                <span class="input-group-text" id="inputGroup-sizing-sm"
                  >Min Price</span
                >
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
                <span class="input-group-text" id="inputGroup-sizing-sm"
                  >Max Price</span
                >
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
                <span class="input-group-text" id="inputGroup-sizing-sm"
                  >Min Rooms</span
                >
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
                <span class="input-group-text" id="inputGroup-sizing-sm"
                  >Max Rooms</span
                >
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
      <br /><br />
      <b-tab title="List" active>
        <ListListingsView
          :listings="filter_satisfying_listings"
          :filters="filters"
        />
      </b-tab>
      <b-tab title="Map">
        <MapListingsView
          :listings="filter_satisfying_listings"
          :filters="filters"
        />
      </b-tab>
    </b-tabs>
    <button class="btn btn-primary" @click="this.get_listings">
      Reload
    </button>
  </div>
</template>

<script>
import axios from "axios";
import ListListingsView from "./ListListingsView.vue";
import MapListingsView from "./MapListingsView.vue";

export default {
  name: "BrowseView",
  props: {
    token: String,
  },
  components: {
    ListListingsView,
    MapListingsView,
  },
  data() {
    return {
      listings: [],
      filters: {
        floor_area_min: "",
        floor_area_max: "",
        price_min: "",
        price_max: "",
        bed_min: "",
        bed_max: "",
      },
    };
  },
  created() {
    this.get_listings();
  },
  computed: {
    filter_satisfying_listings() {
      return this.listings.filter((listing) => this.satisfies_filters(listing));
    },
  },
  methods: {
    satisfies_filters(listing) {
      if (listing === null) {
        return false;
      }
      if (
        this.filters.floor_area_min !== null &&
        this.filters.floor_area_min !== ""
      ) {
        if (listing.floor_area < this.filters.floor_area_min) {
          return false;
        }
      }
      if (
        this.filters.floor_area_max !== null &&
        this.filters.floor_area_max !== ""
      ) {
        if (listing.floor_area > this.filters.floor_area_max) {
          return false;
        }
      }
      if (this.filters.price_min !== null && this.filters.price_min !== "") {
        if (listing.price < this.filters.price_min) {
          return false;
        }
      }
      if (this.filters.price_max !== null && this.filters.price_max !== "") {
        if (listing.price > this.filters.price_max) {
          return false;
        }
      }
      if (this.filters.bed_min !== null && this.filters.bed_min !== "") {
        if (listing.rooms < this.filters.bed_min) {
          return false;
        }
      }
      if (this.filters.bed_max !== null && this.filters.bed_max !== "") {
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
