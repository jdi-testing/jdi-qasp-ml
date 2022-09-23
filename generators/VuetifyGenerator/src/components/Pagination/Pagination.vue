<template>
  <component :is="component" />
</template>

<script>
import CirclePagination from './CirclePagination.vue';
import DisabledPagination from './DisabledPagination.vue';
import LengthPagination from './LengthPagination.vue';
import TotalVisiblePagination from './TotalVisiblePagination.vue';

const variants = [
    CirclePagination,
    DisabledPagination,
    LengthPagination,
    TotalVisiblePagination,
];

export default {
  name: "JdiPagination",

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
