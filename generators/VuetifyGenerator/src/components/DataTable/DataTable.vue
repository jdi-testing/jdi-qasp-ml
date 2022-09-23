<template>
  <component :is="component" />
</template>

<script>
import CrudDataTable from './CrudDataTable.vue';
import CustomFilterDataTable from './CustomFilterDataTable.vue';
import DenseDataTable from './DenseDataTable.vue';
import FilterDataTable from './FilterDataTable.vue';
import GroupingDataTable from './GroupingDataTable.vue';
import HideDefaultHeaderAndFooterDataTable from './HideDefaultHeaderAndFooterDataTable.vue';
import ItemDataTable from './ItemDataTable.vue';
import LoadingDataTable from './LoadingDataTable.vue';
import MultiSortDataTable from './MultiSortDataTable.vue';
import RowSelectionDataTable from './RowSelectionDataTable.vue';
import SearchDataTable from './SearchDataTable.vue';

const variants = [
    CrudDataTable,
    CustomFilterDataTable,
    DenseDataTable,
    FilterDataTable,
    GroupingDataTable,
    HideDefaultHeaderAndFooterDataTable,
    ItemDataTable,
    LoadingDataTable,
    MultiSortDataTable,
    RowSelectionDataTable,
    SearchDataTable,
];

export default {
  name: "JdiDataTable",

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
