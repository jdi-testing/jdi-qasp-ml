<template>
  <v-row>
    <v-badge v-bind="{...data}" :icon="icon" data-label="badge">
      <v-btn class="white--text" color="error" depressed> Lock Account </v-btn>
    </v-badge>
  </v-row>
</template>

<script>
const icons = [
  "mdi-vuetify",
  "mdi-lock",
  "mdi-domain",
  "mdi-dialpad",
  "mdi-email",
];
export default {
  name: "JdiBadge",

  props: {
    data: {
      type: Object,
      default: () => ({
        bordered: false,
        bottom: false,
        dot: false,
        inline: false,
        left: false,
        overlap: false,
        tile: false,
        icon: 0,
      }),
    },
  },

  computed: {
    icon() {
      return icons[this.data.icon];
    },
  },
};
</script>
