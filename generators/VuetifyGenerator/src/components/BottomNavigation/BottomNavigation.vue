<template>
  <component :is="component" />
</template>

<script>
import ColorBottomNavigation from './ColorBottomNavigation.vue';
import GrowBottomNavigation from './GrowBottomNavigation.vue';
import HorizontalBottomNavigation from './HorizontalBottomNavigation.vue';
import ShiftBottomNavigation from './ShiftBottomNavigation.vue';
import ToggleBottomNavigation from './ToggleBottomNavigation.vue';

const variants = [
    ColorBottomNavigation,
    GrowBottomNavigation,
    HorizontalBottomNavigation,
    ShiftBottomNavigation,
    ToggleBottomNavigation,
];

export default {
  name: "JdiBottomNavigation",

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
