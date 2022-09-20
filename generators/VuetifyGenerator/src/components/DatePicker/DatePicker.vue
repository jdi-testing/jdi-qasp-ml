<template>
  <component :is="component" />
</template>

<script>
import AllowedDatesDatePicker from './AllowedDatesDatePicker.vue';
import ColorsDatePicker from './ColorsDatePicker.vue';
import DateEventsDatePicker from './DateEventsDatePicker.vue';
import ElevationDatePicker from './ElevationDatePicker.vue';
import IconsDatePicker from './IconsDatePicker.vue';
import MultipleDatePicker from './MultipleDatePicker.vue';
import RangeDatePicker from './RangeDatePicker.vue';
import ReadonlyDatePicker from './ReadonlyDatePicker.vue';
import ShowSiblingMonthsDatePicker from './ShowSiblingMonthsDatePicker.vue';
import WidthDatePicker from './WidthDatePicker.vue';

const variants = [
    AllowedDatesDatePicker,
    ColorsDatePicker,
    DateEventsDatePicker,
    ElevationDatePicker,
    IconsDatePicker,
    MultipleDatePicker,
    RangeDatePicker,
    ReadonlyDatePicker,
    ShowSiblingMonthsDatePicker,
    WidthDatePicker,
];

export default {
  name: "JdiDatePicker",

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
