<template>
  <component :is="component" />
</template>

<script>
import InsetBottomSheet from './InsetBottomSheet.vue';
import ModelBottomSheet from './ModelBottomSheet.vue';
import MusicPlayerBottomSheet from './MusicPlayerBottomSheet.vue';
import OpenInListBottomSheet from './OpenInListBottomSheet.vue';
import PersistentBottomSheet from './PersistentBottomSheet.vue';

const variants = [
    InsetBottomSheet,
    ModelBottomSheet,
    MusicPlayerBottomSheet,
    OpenInListBottomSheet,
    PersistentBottomSheet
];

export default {
  name: "JdiBottomSheet",

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
