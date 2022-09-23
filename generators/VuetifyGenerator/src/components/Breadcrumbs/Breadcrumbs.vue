<template>
  <component :is="component" />
</template>

<script>
import DashBreadcrumbs from './DashBreadcrumbs.vue';
import DividerBreadcrumbs from './DashBreadcrumbs.vue';
import IconDividerBreadcrumbs from './DashBreadcrumbs.vue';
import LargeBreadcrumbs from './DashBreadcrumbs.vue';

const variants = [
    DashBreadcrumbs,
    DividerBreadcrumbs,
    IconDividerBreadcrumbs,
    LargeBreadcrumbs,
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
