<template>
  <component :is="component" />
</template>

<script>
import AllowedMonthsDatePickerMonth from './AllowedMonthsDatePickerMonth.vue';
import ColorsDatePickerMonth from './ColorsDatePickerMonth.vue';
import IconsDatePickerMonth from './IconsDatePickerMonth.vue';
import MultipleDatePickerMonth from './MultipleDatePickerMonth.vue';
import WidthDatePickerMonth from './WidthDatePickerMonth.vue';

const variants = [
    AllowedMonthsDatePickerMonth,
    ColorsDatePickerMonth,
    IconsDatePickerMonth,
    MultipleDatePickerMonth,
    WidthDatePickerMonth,
];

export default {
  name: "JdiDatePickerMonth",

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
