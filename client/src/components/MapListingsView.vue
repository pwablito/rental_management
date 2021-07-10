<template>
  <div id="maplistingsview">
    This is the map listings view
  </div>
</template>

<script>

export default {
  name: "MapListingsView",
  data() {
    return {
    };
  },
  props: {
      listing: Object,
  },
};
</script>

<style>
.red {
    color: red;
}
.centered {
    text-align: center;
}
</style>
