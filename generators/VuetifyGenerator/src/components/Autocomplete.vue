<template>
  <v-autocomplete
    v-bind="data"
    data-label="autocomplete"
    v-model="values"
    :items="items"
  ></v-autocomplete>
</template>

<script>
export default {
  name: "JdiAutoComplete",

  props: {
    data: {
      type: Object,
      default: () => ({
        'auto-select-first': false,
        chips: false,
        clearable: false,
        'deletable-chips': false,
        dense: false,
        filled: false,
        multiple: false,
        rounded: false,
        'small-chips': false,
        solo: false,
        'solo-inverted': false,
        items: ["foo", "bar", "fizz", "buzz"],
        values: ["foo", "bar"],
        value: null,
      }),
    },
  },
};
</script>

<style></style>
