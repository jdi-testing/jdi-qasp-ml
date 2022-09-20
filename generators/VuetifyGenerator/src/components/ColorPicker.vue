<template>
  <v-color-picker data-label="color-picker" v-bind="data" :mode="mode" />
</template>

<script>
const modes = ["rgba", "hsla", "hexa"];
export default {
  name: "JdiAlert",

  props: {
    data: {
      type: Object,
      default: () => ({
        disabled: false,
        "dot-size": 1,
        "hide-canvas": false,
        "hide-inputs": false,
        "hide-mode-switch": false,
        "hide-sliders": false,
        mode: 0,
        "show-swatches": false,
        "swatches-max-height": 1,
      }),
    },
  },

  computed: {
    mode() {
      return modes[this.data.mode];
    },
  },
};
</script>

<style></style>
