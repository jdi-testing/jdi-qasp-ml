<template>
  <component :is="component" />
</template>

<script>
import BackgroundToolBar from './BackgroundToolBar.vue';
import CollapseToolBar from './CollapseToolBar.vue';
import ContextualToolBar from './ContextualToolBar.vue';
import DenseToolBar from './DenseToolBar.vue';
import ExtendedToolBar from './ExtendedToolBar.vue';
import FlexibleAndCardToolBar from './FlexibleAndCardToolBar.vue';
import FloatingWithSearchToolBar from './FloatingWithSearchToolBar.vue';
import ProminentToolBar from './ProminentToolBar.vue';

const variants = [
    BackgroundToolBar,
    CollapseToolBar,
    ContextualToolBar,
    DenseToolBar,
    ExtendedToolBar,
    FlexibleAndCardToolBar,
    FloatingWithSearchToolBar,
    ProminentToolBar
];

export default {
  name: "JdiToolBar",

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
