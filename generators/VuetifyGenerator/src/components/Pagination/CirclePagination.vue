<template>
  <div class="text-center">
    <v-pagination
      v-model="page"
      :length="4"
      circle
      data-label="pagination"
    ></v-pagination>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        page: 1,
      }
    },
  }
</script>