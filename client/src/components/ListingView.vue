<template>
  <div id="editlistingview">
    <div class="row">
      <div class="col-1 item">
        {{ listing.name }}
      </div>
      <div class="col-1 item">
        {{ listing.realtor }}
      </div>
      <div class="col-3 item">
        {{ listing.description }}
      </div>
      <div class="col-1 item">{{ listing.floor_area }} sq.ft.</div>
      <div class="col-1 item">${{ listing.price }}</div>
      <div class="col-2 item">{{ listing.rooms }}/{{ listing.bathrooms }}</div>
      <div class="col-2 item">
        {{ this.listing_created }}
      </div>
      <div class="col-1 item">
        {{ listing.latitude }}/{{ listing.longitude }}
      </div>
      <div class="col-1 item">
        <div v-if="listing.is_listed">X</div>
      </div>
    </div>
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
            this.toggle_editing();
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
