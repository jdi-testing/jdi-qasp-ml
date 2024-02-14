<template>
  <v-btn data-label="vuetify-btn" v-bind="data">
    {{ data.label }}
  </v-btn>
</template>

<script>
const colors = ['', 'primary', 'error'];
export default {
  name: "JdiButton",

  props: {
    data: {
      type: Object,
      default: () => ({
        color: '',
        label: '',
        text: false,
        block: false,
        disabled: false,
        depressed: false,
        large: false,
        outlined: false,
        plain: false,
        rounded: false,
        tile: false,
        loading: false,
        small: false,
        fab: false,
        'x-large': false,
        'x-small': false,
      }),
    },
  },

  computed: {
    color() {
      return colors[this.data.color];
    },
  }
};
</script>

<style></style>
