<template>
  <v-range-slider v-bind="data" data-label="range-slider"></v-range-slider>
</template>

<script>
export default {
  name: "JdiRangeSlider",

  props: {
    data: {
      type: Object,
      default: () => ({
        dense: false,
        disabled: false,
        "hide-details": false,
        hint: "",
        "inverse-label": false,
        max: 100,
        min: 0,
        "persistent-hint": false,
        readonly: false,
        vertical: false,
      }),
    },
  },
};
</script>

<style></style>
