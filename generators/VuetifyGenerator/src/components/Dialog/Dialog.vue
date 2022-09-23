<template>
  <component :is="component" />
</template>

<script>
import FormDialog from './FormDialog.vue';
import FullScreenDialog from './FullScreenDialog.vue';
import LoadingDialog from './LoadingDialog.vue';
import OverflowedDialog from './OverflowedDialog.vue';
import PersistentDialog from './PersistentDialog.vue';
import ScrollableDialog from './ScrollableDialog.vue';
import TransitionsDialog from './TransitionsDialog.vue';

const variants = [
    FormDialog,
    FullScreenDialog,
    LoadingDialog,
    OverflowedDialog,
    PersistentDialog,
    ScrollableDialog,
    TransitionsDialog,
];

export default {
  name: "JdiDialog",

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
