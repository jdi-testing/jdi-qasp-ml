<template>
  <component :is="component" />
</template>

<script>
import AutoGrowTextArea from './AutoGrowTextArea.vue';
import BackgroundColorTextArea from './BackgroundColorTextArea.vue';
import ClearableTextArea from './ClearableTextArea.vue';
import CounterTextArea from './CounterTextArea.vue';
import IconsTextArea from './IconsTextArea.vue';
import RowsTextArea from './RowsTextArea.vue';

const variants = [
    AutoGrowTextArea,
    BackgroundColorTextArea,
    ClearableTextArea,
    CounterTextArea,
    IconsTextArea,
    RowsTextArea,
];

export default {
  name: "JdiTextArea",

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
