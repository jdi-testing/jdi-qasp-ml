<template>
  <component :is="component" />
</template>

<script>
import ErrorCountInput from './ErrorCountInput.vue';
import HideDetailsInput from './HideDetailsInput.vue';
import LoadingInput from './LoadingInput.vue';
import RulesInput from './RulesInput.vue';
import SuccessInput from './SuccessInput.vue';

const variants = [
    ErrorCountInput,
    HideDetailsInput,
    LoadingInput,
    RulesInput,
    SuccessInput,
];

export default {
  name: "JdiInput",

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
