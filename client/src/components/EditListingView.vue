<template>
  <div id="editlistingview">
    <div class="row">
      <div class="col-1 item">
        {{ listing.name }}
      </div>
      <div class="col-2 item">
        {{ listing.description }}
      </div>
      <div class="col-1 item">{{ listing.floor_area }} sq.ft.</div>
      <div class="col-1 item">${{ listing.price }}</div>
      <div class="col-1 item">{{ listing.rooms }}/{{ listing.bathrooms }}</div>
      <div class="col-2 item">
        {{ this.listing_created }}
      </div>
      <div class="col-1 item">
        {{ listing.latitude }}/{{ listing.longitude }}
      </div>
      <div class="col-1 item">
        <div v-if="listing.is_listed">X</div>
      </div>
      <div class="col-2 item">
        <button @click="toggle_editing" class="btn btn-secondary">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-pencil"
            viewBox="0 0 16 16"
          >
            <path
              d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"
            />
          </svg>
        </button>
        <button @click="delete_listing" class="btn btn-danger">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-trash"
            viewBox="0 0 16 16"
          >
            <path
              d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
            />
            <path
              fill-rule="evenodd"
              d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
            />
          </svg>
        </button>
      </div>
    </div>


    <b-modal
      :id="modal_id"
      title="Edit Listing"
      hide-footer
      v-model="this.editing"
    >
      <form @submit="submit_update_listing">
        <div class="form-group">
          <label for="listing_name">Name</label>
          <input
            type="text"
            v-model="edit_listing.name"
            class="form-control"
            id="listing_name"
            required
          />
        </div>
        <div class="form-group">
          <label for="listing_description">Description</label>
          <input
            type="text"
            v-model="edit_listing.description"
            class="form-control"
            id="listing_description"
          />
        </div>
        <div class="form-group">
          <label for="listing_floor_area">Floor Area (square feet)</label>
          <input
            type="number"
            min="0"
            max="1000000"
            v-model="edit_listing.floor_area"
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
            v-model="edit_listing.price"
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
            v-model="edit_listing.rooms"
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
            v-model="edit_listing.bathrooms"
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
            v-model="edit_listing.latitude"
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
            v-model="edit_listing.longitude"
            class="form-control"
            id="listing_longitude"
            required
          />
        </div>
        <div class="form-group">
          <button class="btn btn-danger" @click="reset_edits">
            Reset
          </button>
          <button class="btn btn-success" type="submit">
            Finished
          </button>
        </div>
      </form>

    <p class="red centered" v-if="this.error_message">
      {{ this.error_message }}
    </p>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";

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
    token: String,
  },
  computed: {
    modal_id() {
      return this.listing.id + "-modal";
    },
    listing_created() {
      return new Date(this.listing.created_on).toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },
  methods: {
    reset() {
      this.edit_listing = Object.assign({}, this.listing);
    },
    update_listing() {
      this.loading = true;
      this.error_message = null;
      axios
        .post("/api/update_listing", {
          listing: this.edit_listing,
          token: this.token,
        })
        .then((response) => {
          if (response.data.success) {
            this.listing = this.edit_listing;
            this.$emit("update_listings");
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
    submit_update_listing(e) {
      e.preventDefault();
      this.update_listing();
    },
    delete_listing() {
      this.loading = true;
      this.error_message = null;
      axios
        .post("/api/delete_listing", {
          id: this.listing.id,
          token: this.token,
        })
        .then((response) => {
          if (response.data.success) {
            this.$emit("update_listings");
          } else {
            this.error_message = response.data.message;
          }
        })
        .catch((err) => {
          console.log(err);
          this.error_message = "Something went wrong";
        })
        .then(() => {
          this.loading = false;
        });
    },
    reset_edits() {
      this.edit_listing = Object.assign({}, this.listing);
    },
    toggle_editing() {
      this.editing = !this.editing;
    },
  },
  created() {
    this.edit_listing = Object.assign({}, this.listing);
  },
};
</script>

<style>
#editlistingview {
  font-size: 10px;
}
.item {
  padding-left: 0px !important;
  padding-right: 0px !important;
}
.red {
  color: red;
}
.centered {
  text-align: center;
}
</style>
