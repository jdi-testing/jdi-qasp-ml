<template>
  <v-checkbox
    v-bind="data"
    data-label="checkbox"
    v-model="checkbox"
  ></v-checkbox>
</template>

<script>
export default {
  name: "JdiCheckbox",

  props: {
    data: {
      type: Object,
      default: () => ({
        color: '',
        label: '',
        indeterminate: false,
        checkbox: true,
      }),
    },
  },
};
</script>

<style></style>
