<template>
  <component :is="component" />
</template>

<script>
import CategoryCalendar from './CategoryCalendar.vue';
import DayBodyCalendar from './DayBodyCalendar.vue';
import DayCalendar from './DayCalendar.vue';
import DaySlotCalendar from './DaySlotCalendar.vue';
import DefaultCalendar from './DefaultCalendar.vue';
import DragAndDropCalendar from './DragAndDropCalendar.vue';
import EventsCalendar from './EventsCalendar.vue';
import WeekCalendar from './WeekCalendar.vue';

const variants = [
    CategoryCalendar,
    DayBodyCalendar,
    DayCalendar,
    DaySlotCalendar,
    DefaultCalendar,
    DragAndDropCalendar,
    EventsCalendar,
    WeekCalendar,
];

export default {
  name: "JdiCalendar",

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
