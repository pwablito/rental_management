<template>
  <div id="createuser">
    <form @submit="create_user">
      <div class="form-group">
        <label for="user_name">Name</label>
        <input
          type="text"
          v-model="user.name"
          class="form-control"
          id="user_name"
          required
        />
      </div>
      <div class="form-group">
        <label for="user_username">Username</label>
        <input
          type="text"
          v-model="user.username"
          class="form-control"
          id="user_username"
          required
        />
      </div>
      <div class="form-group">
        <label for="user_password">Password</label>
        <input
          type="password"
          v-model="user.password"
          class="form-control"
          id="user_password"
          required
        />
      </div>
      <div class="form-group">
        <label for="user_type">Type</label>
        <!-- <b-form-select v-model="this.type_selected" :options="this.options" required >
        </b-form-select> -->
        <b-form-select v-model="type.select.selected">
          <option
            v-for="(select, index) in type.select.options"
            :key="index"
            :value="select">
            {{select}}
          </option>
        </b-form-select>
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
  name: "CreateUserView",
  props: {
    token: String,
  },
  data() {
    return {
      user: {
        name: "",
        username: "",
        password: "",
      },
      error_message: "",
      type: {
        select: {
          selected: "client",
          options: ["client", "realtor", "admin"],
        },
      },
    };
  },
  methods: {
    create_user(e) {
      this.error_message = "";
      e.preventDefault();
      axios
        .post("/api/create_user", {
          token: this.token,
          name: this.user.name,
          username: this.user.username,
          password: this.user.password,
          type: this.type.select.selected,
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
      this.user.name = "";
      this.user.username = "";
      this.user.password = "";
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
