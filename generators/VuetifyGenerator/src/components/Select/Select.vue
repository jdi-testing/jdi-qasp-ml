<template>
  <component :is="component" />
</template>

<script>
import CustomTextAndValueSelect from './CustomTextAndValueSelect.vue';
import DenseSelect from './DenseSelect.vue';
import DisabledSelect from './DisabledSelect.vue';
import IconsSelect from './IconsSelect.vue';
import LightSelect from './LightSelect.vue';
import SelectionSelect from './SelectionSelect.vue';

const variants = [
    CustomTextAndValueSelect,
    DenseSelect,
    DisabledSelect,
    IconsSelect,
    LightSelect,
    SelectionSelect,
];

export default {
  name: "JdiSelect",

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
