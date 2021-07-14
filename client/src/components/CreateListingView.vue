<template>
  <div id="createlisting">
    <form @submit="create_listing">
      <div class="form-group">
        <label for="listing_name">Name</label>
        <input
          type="text"
          v-model="listing.name"
          class="form-control"
          id="listing_name"
          required
        />
      </div>
      <div class="form-group">
        <label for="listing_description">Description</label>
        <input
          type="text"
          v-model="listing.description"
          class="form-control"
          id="listing_description"
        />
      </div>
      <div class="form-group">
        <label for="listing_description">Realtor Name</label>
        <input
          type="text"
          v-model="listing.realtor"
          class="form-control"
          id="listing_realtor"
          required
        />
      </div>
      <div class="form-group">
        <label for="listing_floor_area">Floor Area (square feet)</label>
        <input
          type="number"
          min="0"
          max="1000000"
          v-model="listing.floor_area"
          class="form-control"
          id="listing_floor_area"
          required
        />
      </div>
      <div class="form-group">
        <label for="listing_price">Price per Month in USD</label>
        <input
          type="number"
          min="0"
          max="1000000"
          v-model="listing.price"
          class="form-control"
          id="listing_price"
          required
        />
      </div>
      <div class="form-group">
        <label for="listing_rooms"># Rooms</label>
        <input
          type="number"
          min="0"
          max="100"
          v-model="listing.rooms"
          class="form-control"
          id="listing_rooms"
          required
        />
      </div>
      <div class="form-group">
        <label for="listing_bathrooms"># Bathrooms</label>
        <input
          type="number"
          min="0"
          max="1000"
          v-model="listing.bathrooms"
          class="form-control"
          id="listing_bathrooms"
          required
        />
      </div>
      <div class="form-group">
        <label for="listing_latitude">Latitude</label>
        <input
          type="number"
          min="-90"
          max="90"
          step="0.0001"
          v-model="listing.latitude"
          class="form-control"
          id="listing_latitude"
          required
        />
      </div>
      <div class="form-group">
        <label for="listing_longitude">Longitude</label>
        <input
          type="number"
          min="-180"
          max="180"
          step="0.0001"
          v-model="listing.longitude"
          class="form-control"
          id="listing_longitude"
          required
        />
      </div>
      <div class="form-group centered">
        <button type="submit" class="btn btn-success">Submit</button>
      </div>
    </form>
    <p class="centered red" v-if="this.error_message !== ''">
      {{ this.error_message }}
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateListingView",
  props: {
    token: String,
  },
  data() {
    return {
      listing: {
        name: "",
        description: "",
        floor_area: "",
        price: "",
        rooms: "",
        bathrooms: "",
        latitude: "",
        longitude: "",
        realtor: "",
      },
      error_message: "",
    };
  },
  methods: {
    create_listing(e) {
      this.error_message = "";
      e.preventDefault();
      axios
        .post("/api/create_listing", {
          token: this.token,
          name: this.listing.name,
          description: this.listing.description,
          floor_area: this.listing.floor_area,
          price: this.listing.price,
          rooms: this.listing.rooms,
          bathrooms: this.listing.bathrooms,
          latitude: this.listing.latitude,
          longitude: this.listing.longitude,
          realtor: this.listing.realtor,
        })
        .then((response) => {
          if (response.data.success) {
            alert("Success");
            this.clear();
          } else {
            this.error_message = response.data.message;
          }
        })
        .catch(() => {
          this.error_message = "Something went wrong";
        })
        .then(() => {});
    },
    clear() {
      this.listing.name = "";
      this.listing.description = "";
      this.listing.floor_area = "";
      this.listing.price = "";
      this.listing.rooms = "";
      this.listing.bathrooms = "";
      this.listing.latitude = "";
      this.listing.longitude = "";
      this.listing.realtor = "";
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
