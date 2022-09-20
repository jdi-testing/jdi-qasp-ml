<template>
  <component :is="component" />
</template>

<script>
import DisabledHover from './DisabledHover.vue';
import HoverListHover from './HoverListHover.vue';
import OpenAndCloseDelayHover from './OpenAndCloseDelayHover.vue';
import TransitionHover from './TransitionHover.vue';

const variants = [
    DisabledHover,
    HoverListHover,
    OpenAndCloseDelayHover,
    TransitionHover
];

export default {
  name: "JdiHover",

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
