<template>
  <div id="editusers" class="centered">
    <div v-for="user in this.users" :key="user.username">
      <hr>
      <EditUserView :user="user" :token="token" @update_users="get_users" />
      <hr>
    </div>

    <button class="btn btn-primary" @click="this.get_users">
      Reload
    </button>
  </div>
</template>

<script>
import axios from "axios";
import EditUserView from "./EditUserView.vue";

export default {
  name: "EditusersView",
  props: {
    token: String,
  },
  components: {
    EditUserView,
  },
  data() {
    return {
      users: [],
    };
  },
  created() {
    this.get_users();
  },
  methods: {
    get_users() {
      this.loading = true;
      this.error_message = null;
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
.centered {
  text-align: center;
}
.red {
  color: red;
}
</style>
