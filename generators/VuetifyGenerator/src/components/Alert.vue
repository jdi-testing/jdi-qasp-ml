<template>
  <v-alert data-label="alerts" v-bind="data" :type="type">
    {{ data.text }}
  </v-alert>
</template>

<script>
const types = ["success", "info", "warning", "error"];
const borders = ["top", "right", "bottom", "left"];
export default {
  name: "JdiAlert",

  props: {
    data: {
      type: Object,
      default: () => ({
        type: "success",
        text: "",
        shaped: false,
        dense: false,
        prominent: false,
        outlined: false,
        dissmissible: false,
        "colored-border": false,
        border: '',
      }),
    },
  },

    computed: {
        type() {
            return types[this.data.type];
        },
        border() {
            return borders[this.data.border];
        }
    }
};
</script>

<style></style>
