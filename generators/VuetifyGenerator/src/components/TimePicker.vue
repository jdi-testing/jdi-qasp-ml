<template>
  <v-time-picker data-label="time-picker" v-bind="data" :format="format">
    {{ data.text }}
  </v-time-picker>
</template>

<script>
const formats = ["ampm", "24hr"];
export default {
  name: "JdiTimePicker",

  props: {
    data: {
      type: Object,
      default: () => ({
        "ampm-in-title": false,
        disabled: false,
        format: 0,
        "full-width": false,
        landscape: false,
        "no-title": false,
        readonly: false,
        scrollable: false,
        "use-seconds": false,
      }),
    },
  },

  computed: {
    format() {
      return formats[this.data.format];
    },
  },
};
</script>
