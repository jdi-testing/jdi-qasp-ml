<template>
  <component :is="component" />
</template>

<script>
import DefaultAppBar from "./DefaultAppBar.vue";
import CollapsibleAppBar from "./CollapsibleAppBar.vue";
import DenseAppBar from "./DenseAppBar.vue";
import ElevateOnScrollAppBar from "./ElevateOnScrollAppBar.vue";
import FadeImageOnScrollAppBar from "./FadeImageOnScrollAppBar.vue";
import HideOnScrollAppBar from "./HideOnScrollAppBar.vue";
import ProminentAppBar from "./ProminentAppBar.vue";

const variants = [
  DefaultAppBar,
  CollapsibleAppBar,
  DenseAppBar,
  ElevateOnScrollAppBar,
  FadeImageOnScrollAppBar,
  HideOnScrollAppBar,
  ProminentAppBar,
];

export default {
  name: "JdiAppBar",

  components: {
    ...variants,
  },

  props: {
    data: {
        type: Object,
        default: () => ({
            type: 0,
        })
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
