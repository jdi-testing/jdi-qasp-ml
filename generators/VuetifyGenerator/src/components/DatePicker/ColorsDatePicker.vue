<template>
  <v-row justify="space-around">
    <v-date-picker
      v-model="picker"
      color="green lighten-1"
      data-label="date-picker"
    ></v-date-picker>
    <v-date-picker
      v-model="picker2"
      color="green lighten-1"
      header-color="primary"
      data-label="date-picker"
    ></v-date-picker>
  </v-row>
</template>

<script>
  export default {
    data () {
      return {
        picker: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        picker2: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      }
    },
  }
</script>