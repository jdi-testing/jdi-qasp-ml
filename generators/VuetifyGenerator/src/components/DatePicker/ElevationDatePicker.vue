<template>
  <v-row
    justify="space-around"
    align="center"
  >
    <v-date-picker
      v-model="picker"
      flat
      data-label="date-picker"
    ></v-date-picker>

    <v-date-picker
      v-model="picker"
      elevation="15"
      data-label="date-picker"
    ></v-date-picker>
  </v-row>
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