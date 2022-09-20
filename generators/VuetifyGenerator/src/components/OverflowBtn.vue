<template>
  <v-overflow-btn v-bind="data" data-label="overflow-btn"></v-overflow-btn>
</template>

<script>
export default {
  name: "JdiOverflowBtn",

  props: {
    data: {
      type: Object,
      default: () => ({
        dense: false,
        disabled: false,
        editable: false,
        filled: false,
        loading: false,
        overflow: false,
        "persistent-hint": false,
        label: '',
        readonly: false,
        reverse: false,
        segmented: false,
      }),
    },
  },
};
</script>
