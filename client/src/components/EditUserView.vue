<template>
  <div id="edituserview">
    <div class="row">
      <div class="col-1"></div>
      <div class="col-2 item">{{ user.name }}</div>
      <div class="col-2 item">{{ user.username }}</div>
      <div class="col-2 item">{{ this.user_created }}</div>
      <div class="col-2 item">{{ user.type }}</div>
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
        <button @click="delete_user" class="btn btn-danger">
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
      <div class="col-1"></div>
    </div>

    <b-modal title="Edit User" hide-footer v-model="editing">
      <form @submit="submit_update_user">
        <div class="form-group">
          <label for="user_name">Name</label>
          <input
            type="text"
            v-model="edit_user.name"
            class="form-control"
            id="user_name"
            required
          />
        </div>
        <div class="form-group">
          <label for="user_username">Username</label>
          <input
            type="text"
            v-model="edit_user.username"
            class="form-control"
            id="user_username"
            required
          />
        </div>
        <div class="form-group">
          <label for="user_password">Password</label>
          <input
            type="password"
            v-model="edit_password"
            class="form-control"
            id="user_password"
          />
        </div>
        <div class="form-group">
        <label for="user_type">Type</label>
        <b-form-select v-model="edit_user.type">
          <option
            v-for="(select, index) in type.select.options"
            :key="index"
            :value="select"
          >
            {{ select }}
          </option>
        </b-form-select>
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
  name: "EdituserView",
  data() {
    return {
      editing: false,
      edit_user: {},
      edit_password: "",
      loading: false,
      error_message: null,
      type: {
        select: {
          options: ["client", "realtor", "admin"],
        },
      },
    };
  },
  props: {
    user: Object,
    token: String,
  },
  computed: {
    user_created() {
      return new Date(this.user.created_on).toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },
  methods: {
    reset() {
      this.edit_user = Object.assign({}, this.user);
    },
    update_user() {
      this.loading = true;
      this.error_message = null;
      let data = {
        user: this.edit_user,
        token: this.token,
      }
      if (this.edit_password !== "") {
        data.password = this.edit_password;
      }
      axios
        .post("/api/update_user", data)
        .then((response) => {
          if (response.data.success) {
            this.toggle_editing();
            this.$emit("update_users");
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
    submit_update_user(e) {
      e.preventDefault();
      this.update_user();
    },
    delete_user() {
      this.loading = true;
      this.error_message = null;
      axios
        .post("/api/delete_user", {
          id: this.user.id,
          token: this.token,
        })
        .then((response) => {
          if (response.data.success) {
            this.$emit("update_users");
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
      this.edit_user = Object.assign({}, this.user);
      this.edit_password = "";
    },
    toggle_editing() {
      this.editing = !this.editing;
    },
  },
  created() {
    this.edit_user = Object.assign({}, this.user);
  },
};
</script>

<style>
#edituserview {
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
