<template>
  <v-chip data-label="chip" v-bind="data">
    {{ data.label }}
  </v-chip>
</template>

<script>
export default {
  name: "JdiButton",

  props: {
    data: {
      type: Object,
      default: () => ({
        filter: false,
        color: '',
        label: false,
        link: false,
        outlined: false,
        pill: false,
        close: false,
        draggable: false,
        'filter-icon': "mdi-plus"
      }),
    },
  },
};
</script>

<style></style>
