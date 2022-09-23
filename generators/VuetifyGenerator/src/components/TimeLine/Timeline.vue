<template>
  <component :is="component" />
</template>

<script>
import AdvancedTimeline from './AdvancedTimeline.vue';
import ColorTimeline from './ColorTimeline.vue';
import DenseTimeline from './DenseTimeline.vue';
import IconDotsTimeline from './IconDotsTimeline.vue';
import OppositeTimeline from './OppositeTimeline.vue';
import ReverseTimeline from './ReverseTimeline.vue';
import SmallTimeline from './SmallTimeline.vue';

const variants = [
    AdvancedTimeline,
    ColorTimeline,
    DenseTimeline,
    IconDotsTimeline,
    OppositeTimeline,
    ReverseTimeline,
    SmallTimeline,
];

export default {
  name: "JdiTimeline",

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
