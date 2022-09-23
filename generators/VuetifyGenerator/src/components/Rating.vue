<template>
  <v-rating
    data-label="rating"
    v-bind="data"
    :empty-icon="emptyIcon"
    :full-icon="fullIcon"
    :half-icon="halfIcon"
  />
</template>

<script>
const emptyIcons = ["mdi-star-outline", "mdi-heart-outline"];
const fullIcons = ["mdi-heart", "mdi-star"];
const halfIcons = ["mdi-heart-half-full", "mdi-star-half-full"];
export default {
  name: "JdiRating",

  props: {
    data: {
      type: Object,
      default: () => ({
        dense: false,
        "empty-icon": 0,
        "full-icon": 0,
        "half-icon": 0,
        "half-increments": false,
        hover: false,
        length: 2,
        readonly: false,
        size: 30,
        value: 0,
      }),
    },
  },

  computed: {
    fullIcon() {
      return fullIcons[this.data["full-icon"]];
    },
    halfIcon() {
      return halfIcons[this.data["half-icon"]];
    },
    emptyIcon() {
      return emptyIcons[this.data["empty-icon"]];
    },
  },
};
</script>
