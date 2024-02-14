<template>
  <component :is="component" />
</template>

<script>
import AcceptFileInput from './AcceptFileInput.vue';
import ChipsFileInput from './ChipsFileInput.vue';
import CounterFileInput from './CounterFileInput.vue';
import DenseFileInput from './DenseFileInput.vue';
import MultipleFileInput from './MultipleFileInput.vue';
import PrependFileInput from './PrependFileInput.vue';
import ShowSizeFileInput from './ShowSizeFileInput.vue';
import ValidationFileInput from './ValidationFileInput.vue';

const variants = [
    AcceptFileInput,
    ChipsFileInput,
    CounterFileInput,
    DenseFileInput,
    MultipleFileInput,
    PrependFileInput,
    ShowSizeFileInput,
    ValidationFileInput,
];

export default {
  name: "JdiFileInput",

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
