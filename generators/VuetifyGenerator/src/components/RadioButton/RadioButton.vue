<template>
  <component :is="component" />
</template>

<script>
import ColorRadioButton from './ColorRadioButton.vue';
import LabeledRadioButton from './LabeledRadioButton.vue';

const variants = [
    ColorRadioButton,
    LabeledRadioButton,
];

export default {
  name: "JdiRadioButton",

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
