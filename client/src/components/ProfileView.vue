<template>
  <div id="profileview">
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
                  <td>{{user.created_on}}</td>
              </tr>
          </tbody>
      </table>
  </div>
</template>

<script>

export default {
  name: 'ProfileView',
  props: {
      user: Object,
      token: String,
  },
}
</script>

<style>
table {
    width: 100%;
    text-align: center;
}
</style>
