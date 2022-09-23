<template>
  <v-card
    class="pa-4"
    flat
    height="300px"
    img="https://cdn.vuetifyjs.com/images/toolbar/map.jpg"
    data-label="card"
  >
    <v-toolbar
      dense
      floating
      data-label="toolbar"
    >
      <v-text-field
        hide-details
        prepend-icon="mdi-magnify"
        single-line
        data-label="text-field"
      ></v-text-field>

      <v-btn icon>
        <v-icon>mdi-crosshairs-gps</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-toolbar>
  </v-card>
</template>