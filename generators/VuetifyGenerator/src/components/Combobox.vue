<template>
  <v-combobox
    v-bind="data"
    data-label="combobox"
    v-model="select"
    :items="items"
  ></v-combobox>
</template>

<script>
export default {
  name: "JdiCombobox",

  props: {
    data: {
      type: Object,
      default: () => ({
        select: ["Vuetify", "Programming"],
        items: ["Programming", "Design", "Vue", "Vuetify"],
        clearable: false,
        dense: false,
        filled: false,
        "hide-selected": false,
        multiple: false,
        outlined: false,
        "persistent-hint": false,
        "small-chips": false,
        solo: false,
        label: '',
      }),
    },
  },
};
</script>

<style></style>
