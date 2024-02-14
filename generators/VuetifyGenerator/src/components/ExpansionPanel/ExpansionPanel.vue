<template>
  <component :is="component" />
</template>

<script>
import AccordionExpansionPanel from './AccordionExpansionPanel.vue';
import AdvancedExpansioPanel from './AdvancedExpansionPanel.vue';
import DisabledExpansionPanel from './DisabledExpansionPanel.vue';
import FocusableExpansionPanel from './FocusableExpansionPanel.vue';
import InsetExpansionPanel from './InsetExpansionPanel.vue';
import PopoutExpansionPanel from './PopoutExpansionPanel.vue';

const variants = [
    AccordionExpansionPanel,
    AdvancedExpansioPanel,
    DisabledExpansionPanel,
    FocusableExpansionPanel,
    InsetExpansionPanel,
    PopoutExpansionPanel,
];

export default {
  name: "JdiExpansionPanel",

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
