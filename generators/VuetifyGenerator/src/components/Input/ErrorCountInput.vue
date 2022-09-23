<template>
  <v-input
    error-count="2"
    :error-messages="['Fatal error', 'Another error']"
    error
    disabled
    data-label="input"
  >
    Input
  </v-input>
</template>