<template>
  <component :is="component" />
</template>

<script>
import AlignWithTitleTabs from './AlignWithTitleTabs.vue';
import CenterActiveTabs from './CenterActiveTabs.vue';
import CustomIconsTabs from './CustomIconsTabs.vue';
import DesktopTabs from './DesktopTabs.vue';
import FixedTabs from './FixedTabs.vue';
import GrowTabs from './GrowTabs.vue';
import IconsAndTextTabs from './IconsAndTextTabs.vue';
import OverflowToMenuTabs from './OverflowToMenuTabs.vue';
import PaginationTabs from './PaginationTabs.vue';
import VerticalTabs from './VerticalTabs.vue';

const variants = [
    AlignWithTitleTabs,
    CenterActiveTabs,
    CustomIconsTabs,
    DesktopTabs,
    FixedTabs,
    GrowTabs,
    IconsAndTextTabs,
    OverflowToMenuTabs,
    PaginationTabs,
    VerticalTabs,
];

export default {
  name: "JdiTabs",

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
