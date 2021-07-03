<template>
  <div class="loginregister">
    <div class="register" v-if="this.registering">
      <h2 class="centered">Register</h2>
      <form @submit="register">
        <div class="form-group">
          <label for="name_input">Name</label>
          <input
            type="text"
            v-bind="name"
            class="form-control"
            id="name_input"
          />
        </div>
        <div class="form-group">
          <label for="username_input">Username</label>
          <input
            type="text"
            v-bind="username"
            class="form-control"
            id="username_input"
          />
        </div>
        <div class="form-group">
          <label for="password_input">Password</label>
          <input
            type="password"
            v-bind="password"
            class="form-control"
            id="password_input"
          />
        </div>
        <div class="form-group centered">
          <button type="submit" class="btn btn-success">Submit</button>
        </div>
      </form>
      <p>Already have an account? <button @click="this.toggle_login_register">login</button> now.
    </div>
    <div class="login" v-else>
      <h2 class="centered">Login</h2>
      <form @submit="login">
        <div class="form-group">
          <label for="username_input">Username</label>
          <input
            type="text"
            v-bind="username"
            class="form-control"
            id="username_input"
          />
        </div>
        <div class="form-group">
          <label for="password_input">Password</label>
          <input
            type="password"
            v-bind="password"
            class="form-control"
            id="password_input"
          />
        </div>
        <div class="form-group centered">
          <button type="submit" class="btn btn-success">Submit</button>
        </div>
      </form>
      <p>Don't have an account? <button @click="this.toggle_login_register">register</button> now.
    </div>
    <p class="red" v-if="this.error_message !== ''">
      {{ this.error_message }}
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginRegister",
  props: {
    user: Object,
  },
  data() {
    return {
      name: "",
      username: "",
      password: "",
      error_message: "",
      registering: false,
    };
  },
  methods: {
    toggle_login_register() {
      this.registering = !this.registering;
    },
    register(e) {
      e.preventDefault(); // Keep page from reloading
      this.error_message = null;
      // TODO make sure all fields are filled out
      axios
        .post("/api/register", {
          username: this.username,
          name: this.name,
          password: this.password,
        })
        .then((response) => {
          if (response.data.success) {
            this.user = response.data.user;
          } else {
            this.error_message = response.data.message;
          }
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    login(e) {
      e.preventDefault(); // Keep page from reloading
      this.error_message = null;
      // TODO make sure all fields are filled out
      axios
        .post("/api/login", {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          if (response.data.success) {
            this.user = response.data.user;
          } else {
            this.error_message = response.data.message;
          }
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.red {
  color: red;
}

.centered {
  text-align: center;
}
</style>
