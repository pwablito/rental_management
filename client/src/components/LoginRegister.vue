<template>
  <div class="loginregister">
    <div class="register" v-if="this.registering">
      <h2 class="centered">Register</h2>
      <form @submit="register">
        <div class="form-group">
          <label for="register_name_input">Name</label>
          <input
            type="text"
            v-model="input.register.name"
            class="form-control"
            id="register_name_input"
          />
        </div>
        <div class="form-group">
          <label for="register_username_input">Username</label>
          <input
            type="text"
            v-model="input.register.username"
            class="form-control"
            id="register_username_input"
          />
        </div>
        <div class="form-group">
          <label for="register_password_input">Password</label>
          <input
            type="password"
            v-model="input.register.password"
            class="form-control"
            id="register_password_input"
          />
        </div>
        <div class="form-group centered">
          <button type="submit" class="btn btn-success">Submit</button>
        </div>
      </form>
      <p>
        Already have an account?
        <button @click="this.toggle_login_register">login</button> now.
      </p>
    </div>
    <div class="login" v-else>
      <h2 class="centered">Login</h2>
      <form @submit="login">
        <div class="form-group">
          <label for="login_username_input">Username</label>
          <input
            type="text"
            v-model="input.login.username"
            class="form-control"
            id="login_username_input"
          />
        </div>
        <div class="form-group">
          <label for="login_password_input">Password</label>
          <input
            type="password"
            v-model="input.login.password"
            class="form-control"
            id="login_password_input"
          />
        </div>
        <div class="form-group centered">
          <button type="submit" class="btn btn-success">Submit</button>
        </div>
      </form>
      <p>
        Don't have an account?
        <button @click="this.toggle_login_register">register</button> now.
      </p>
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
  data() {
    return {
      input: {
        register: {
          name: "",
          username: "",
          password: "",
        },
        login: {
          username: "",
          password: "",
        },
      },
      error_message: "",
      registering: false,
    };
  },
  methods: {
    toggle_login_register() {
      this.registering = !this.registering;
      this.error_message = null;
    },
    register(e) {
      e.preventDefault(); // Keep page from reloading
      this.error_message = null;
      if (
        this.input.register.name === "" ||
        this.input.register.uesrname === "" ||
        this.input.register.password === ""
      ) {
        this.error_message = "Please fill out all fields";
      } else {
        axios
          .post("/api/register", {
            username: this.input.register.username,
            name: this.input.register.name,
            password: this.input.register.password,
          })
          .then((response) => {
            if (response.data.success) {
              this.$emit("set_user", {user: response.data.user});
              this.$emit("set_token", {token: response.data.token});
            } else {
              this.error_message = response.data.message;
            }
          })
          .catch(() => {
            this.error_message = "Something went wrong";
          });
      }
    },
    login(e) {
      e.preventDefault(); // Keep page from reloading
      this.error_message = null;
      if (
        this.input.login.username === "" ||
        this.input.login.password === ""
      ) {
        this.error_message = "Please fill out all fields";
      } else {
        axios
          .post("/api/login", {
            username: this.input.login.username,
            password: this.input.login.password,
          })
          .then((response) => {
            if (response.data.success) {
              this.$emit("set_user", {user: response.data.user});
              this.$emit("set_token", {token: response.data.token});
            } else {
              this.error_message = response.data.message;
            }
          })
          .catch(() => {
            this.error_message = "Something went wrong";
          });
      }
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
