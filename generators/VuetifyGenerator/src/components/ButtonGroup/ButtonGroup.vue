<template>
  <component :is="component" />
</template>

<script>
import MandatoryButtonGroup from "./MandatoryButtonGroup.vue";
import MultipleButtonGroup from "./MultipleButtonGroup.vue";
import RoundedButtonGroup from "./RoundedButtonGroup.vue";
import ToolBarButtonGroup from "./ToolBarButtonGroup.vue";

const variants = [
  MandatoryButtonGroup,
  MultipleButtonGroup,
  RoundedButtonGroup,
  ToolBarButtonGroup,
];

export default {
  name: "JdiButtonGroup",

  components: {
    ...variants,
  },

  props: {
    data: {
      type: Object,
      default: () => ({
        type: 0,
      }),
    },
  },

  computed: {
    component() {
      return variants[this.data.type];
    },
  },
};
</script>

<style></style>
