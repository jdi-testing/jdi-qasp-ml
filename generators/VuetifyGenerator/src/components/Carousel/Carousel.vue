<template>
  <component :is="component" />
</template>

<script>
import CustomDelimetersCarousel from './CustomDelimetersCarousel.vue';
import CustomizedArrowsCarousel from './CustomizedArrowsCarousel.vue';
import CustomTransitionCarousel from './CustomTransitionCarousel.vue';
import CycleCarousel from './CycleCarousel.vue';
import HideControlsCarousel from './HideControlsCarousel.vue';
import HideDelimetersCarousel from './HideDelimetersCarousel.vue';

const variants = [
    CustomDelimetersCarousel,
    CustomizedArrowsCarousel,
    CustomTransitionCarousel,
    CycleCarousel,
    HideControlsCarousel,
    HideDelimetersCarousel
];

export default {
  name: "JdiCarousel",

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
