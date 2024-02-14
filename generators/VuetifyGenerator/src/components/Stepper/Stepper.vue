<template>
  <component :is="component" />
</template>

<script>
import AlternateLabelWithErrorsStepper from './AlternateLabelWithErrorsStepper.vue';
import NonLinearStepper from './NonLinearStepper.vue';
import OptionalStepStepper from './OptionalStepStepper.vue';
import VerticalStepper from './VerticalStepper.vue';

const variants = [
    AlternateLabelWithErrorsStepper,
    NonLinearStepper,
    OptionalStepStepper,
    VerticalStepper,
];

export default {
  name: "JdiStepper",

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
