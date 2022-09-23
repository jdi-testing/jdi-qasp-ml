<template>
  <v-date-picker
    v-model="picker"
    show-adjacent-months
    data-label="date-picker"
  ></v-date-picker>
</template>

<script>
  export default {
    data () {
      return {
        picker: null,
      }
    },
  }
</script>