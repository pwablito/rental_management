<template>
  <div id="profileview" class="centered">
      <table>
          <tbody>
              <tr>
                  <td>Username</td>
                  <td>{{user.username}}</td>
              </tr>
              <tr>
                  <td>Role</td>
                  <td>{{user.type}}</td>
              </tr>
              <tr>
                  <td>Name</td>
                  <td>{{user.name}}</td>
              </tr>
              <tr>
                  <td>Created</td>
                  <td>{{user_created}}</td>
              </tr>
          </tbody>
      </table>
      <button class="btn btn-danger" @click="logout">Logout</button>
  </div>
</template>

<script>

export default {
  name: 'ProfileView',
  props: {
      user: Object,
      token: String,
  },
  methods: {
      logout() {
          this.$emit("logout");
      }
  },
  computed: {
    user_created() {
      return new Date(
        this.user.created_on
      ).toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric"
      })
    }
  },
}
</script>

<style>
table {
    width: 100%;
    text-align: center;
}
.centered {
    text-align: center;
}
</style>
