<template>
  <component :is="component" />
</template>

<script>
import ActionStackList from './ActionStackList.vue';
import DenseList from './DenseList.vue';
import DisabledList from './DisabledList.vue';
import ExpansionList from './ExpansionList.vue';
import FlatList from './FlatList.vue';
import NavList from './NavList.vue';
import RoundedList from './RoundedList.vue';
import ShapedList from './ShapedList.vue';
import SingleLineList from './SingleLineList.vue';
import SubGroupList from './SubGroupList.vue';
import ThreeLineList from './ThreeLineList.vue';
import TwoLinesAndSubHeaderList from './TwoLinesAndSubHeaderList.vue';

const variants = [
    ActionStackList,
    DenseList,
    DisabledList,
    ExpansionList,
    FlatList,
    NavList,
    RoundedList,
    ShapedList,
    SingleLineList,
    SubGroupList,
    ThreeLineList,
    TwoLinesAndSubHeaderList,
];

export default {
  name: "JdiList",

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
