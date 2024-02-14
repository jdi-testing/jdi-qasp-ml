<template>
  <v-switch v-bind="data" data-label="switch"></v-switch>
</template>

<script>
export default {
  name: "JdiSwitch",

  props: {
    data: {
      type: Object,
      default: () => ({
        color: '',
        flat: false,
        inset: false,
        loading: false,
      }),
    },
  },
};
</script>

<style></style>
