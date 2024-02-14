<template>
  <component :is="component" />
</template>

<script>
import ActivatableTreeview from './ActivatableTreeview.vue';
import AppendAndLabelTreeview from './AppendAndLabelTreeview.vue';
import ColorTreeview from './ColorTreeview.vue';
import DenseModeTreeview from './DenseModeTreeview.vue';
import HoverableTreeview from './HoverableTreeview.vue';
import ItemDisalbedTreeview from './ItemDisabledTreeview.vue';
import SearchAndFilterTreeview from './SearchAndFilterTreeview.vue';
import SelectableTreeview from './SelectableTreeview.vue';
import SelectionTypeTreeview from './SelectionTypeTreeview.vue';

const variants = [
    ActivatableTreeview,
    AppendAndLabelTreeview,
    ColorTreeview,
    DenseModeTreeview,
    HoverableTreeview,
    ItemDisalbedTreeview,
    SearchAndFilterTreeview,
    SelectableTreeview,
    SelectionTypeTreeview
];

export default {
  name: "JdiTreeview",

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
