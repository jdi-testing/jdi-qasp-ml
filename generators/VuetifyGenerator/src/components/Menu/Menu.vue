<template>
  <component :is="component" />
</template>

<script>
import AbsoluteMenu from './AbsoluteMenu.vue';
import ComponentMenuf from './ComponentMenu.vue';
import MenuAsPopoverMenu from './MenuAsPopoverMenu.vue';
import RoundedMenu from './RoundedMenu.vue';

const variants = [
    AbsoluteMenu,
    ComponentMenuf,
    MenuAsPopoverMenu,
    RoundedMenu
];

export default {
  name: "JdiMenu",

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
