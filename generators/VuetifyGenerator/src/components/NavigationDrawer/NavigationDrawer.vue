<template>
  <component :is="component" />
</template>

<script>
import BottomNavigationDrawer from './BottomNavigationDrawer.vue';
import ColoredNavigationDrawer from './ColoredNavigationDrawer.vue';
import CombinedNavigationDrawer from './CombinedNavigationDrawer.vue';
import ExpandOnHoverNavigationDrawer from './ExpandOnHoverNavigationDrawer.vue';
import ImagesNavigationDrawer from './ImagesNavigationDrawer.vue';
import PermanentAndFloatingNavigationDrawer from './PermanentAndFloatingNavigationDrawer.vue';

const variants = [
    BottomNavigationDrawer,
    ColoredNavigationDrawer,
    CombinedNavigationDrawer,
    ExpandOnHoverNavigationDrawer,
    ImagesNavigationDrawer,
    PermanentAndFloatingNavigationDrawer,
];

export default {
  name: "JdiNavigationDrawer",

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
