<template>
  <component :is="component" />
</template>

<script>
import ColumnChipGroup from './ColumnChipGroup.vue';
import FilterResultsChipGroup from './FilterResultsChipGroup.vue';
import MultipleChipGroup from './MultipleChipGroup.vue';

const variants = [
    ColumnChipGroup,
    FilterResultsChipGroup,
    MultipleChipGroup
];

export default {
  name: "JdiChipGroup",

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
