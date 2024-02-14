<template>
  <component :is="component" />
</template>

<script>
import ClearableTextField from './ClearableTextField.vue'
import CounterTextField from './CounterTextField.vue';
import CustomColorsTextField from './CustomColorsTextField.vue';
import DenseTextField from './DenseTextField.vue';
import DisabledAndReadonlyTextField from './DisabledAndReadonlyTextField.vue';
import FilledTextField from './FilledTextField.vue';
import HideDetailsTextField from './HideDetailsTextField.vue';
import HintTextField from './HintTextField.vue';
import IconsTextField from './IconsTextField.vue';
import OutlinedTextField from './OutlinedTextField.vue';
import PasswordTextField from './PasswordTextField.vue';
import PrefixesAndSuffixesTextField from './PrefixesAndSuffixesTextField.vue';
import ProgressTextField from './ProgressTextField.vue';
import ShapedTextField from './ShapedTextField.vue';
import SoloTextField from './SoloTextField.vue';
import ValidationTextField from './ValidationTextField.vue';

const variants = [
    ClearableTextField,
    CounterTextField,
    CustomColorsTextField,
    DenseTextField,
    DisabledAndReadonlyTextField,
    FilledTextField,
    HideDetailsTextField,
    HintTextField,
    IconsTextField,
    OutlinedTextField,
    PasswordTextField,
    PrefixesAndSuffixesTextField,
    ProgressTextField,
    ShapedTextField,
    SoloTextField,
    ValidationTextField
];

export default {
  name: "JdiTextField",

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
