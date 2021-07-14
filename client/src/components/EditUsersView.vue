<template>
  <div id="editusersview" class="centered">
    <div class="row">
      <div class="col-1"></div>
      <div class="col-2 item">Name</div>
      <div class="col-2 item">Username</div>
      <div class="col-2 item">Created On</div>
      <div class="col-2 item">Type</div>
      <div class="col-2 item">Edit/Delete</div>
      <div class="col-1"></div>
    </div>
    <hr />
    <div v-for="user in this.users" :key="user.username">
        <EditUserView
          :user="user"
          :token="token"
          @update_users="get_users"
        />
        <hr />
    </div>

    <button class="btn btn-primary" @click="this.get_users">
      Reload
    </button>


      <p class="red centered" v-if="this.error_message">
        {{ this.error_message }}
      </p>
  </div>
</template>

<script>
import axios from "axios";
import EditUserView from "./EditUserView.vue";

export default {
  name: "EditUsersView",
  props: {
    token: String,
  },
  components: {
    EditUserView,
  },
  data() {
    return {
      users: [],
      error_message: "",
      loading: false,
    };
  },
  created() {
    this.get_users();
  },
  methods: {
    get_users() {
      this.loading = true;
      this.error_message = null;
      this.users = [];
      axios
        .post("/api/get_users", {
          token: this.token,
        })
        .then((response) => {
          if (response.data.success) {
            this.users = response.data.users;
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
