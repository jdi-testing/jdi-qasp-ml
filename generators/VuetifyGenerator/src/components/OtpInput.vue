<template>
  <v-otp-input v-bind="data" data-label="otp-input"></v-otp-input>
</template>

<script>
const types = ['text', 'password', 'number'];
export default {
  name: "JdiOtpInput",

  props: {
    data: {
      type: Object,
      default: () => ({
        dark: false,
        disabled: false,
        plain: false,
        length: 2,
        type: 0,
      }),
    },
  },

  computed: {
    type() {
      return types[this.data.type];
    },
  },
};
</script>
