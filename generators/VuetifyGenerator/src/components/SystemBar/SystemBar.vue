<template>
  <component :is="component" />
</template>

<script>
import ColorSystemBar from './ColorSystemBar.vue';
import DarkStatusSystemBar from './DarkStatusSystemBar.vue';
import LightsOutSystemBar from './LightsOutSystemBar.vue';
import WindowStatusBar from './WindowStatusBar.vue';

const variants = [
    ColorSystemBar,
    DarkStatusSystemBar,
    LightsOutSystemBar,
    WindowStatusBar
];

export default {
  name: "JdiSystemBar",

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
