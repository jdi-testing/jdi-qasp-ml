<template>
  <component :is="component" />
</template>

<script>
import CustomizedArrowsWindow from './CustomizedArrowsWindow.vue';
import DefaultWindow from './DefaultWindow.vue';
import OnboardingWindow from './OnboardingWindow.vue';
import ReverseWindow from './ReverseWindow.vue';
import VerticalWindow from './VerticalWindow.vue';

const variants = [
    CustomizedArrowsWindow,
    DefaultWindow,
    OnboardingWindow,
    ReverseWindow,
    VerticalWindow,
];

export default {
  name: "JdiWindow",

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
