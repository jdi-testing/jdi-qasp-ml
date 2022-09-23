<template>
  <component :is="component" />
</template>

<script>
import DarkSimpleTable from './DarkSimpleTable.vue';
import DenseSimpleTable from './DenseSimpleTable.vue';
import FixedHeaderSimpleTable from './FixedHeaderSimpleTable.vue';
import HeightSimpleTable from './HeightSimpleTable.vue';

const variants = [
    DarkSimpleTable,
    DenseSimpleTable,
    FixedHeaderSimpleTable,
    HeightSimpleTable,
];

export default {
  name: "JdiSimpleTable",

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
