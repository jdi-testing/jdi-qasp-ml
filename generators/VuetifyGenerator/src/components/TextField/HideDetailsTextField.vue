<template>
  <div>
    <v-text-field
      label="Main input"
      :rules="rules"
      hide-details="auto"
      data-label="text-field"
    ></v-text-field>
    <v-text-field label="Another input" data-label="text-field"></v-text-field>
  </div>
</template>

<script>
  export default {
    data: () => ({
      rules: [
        value => !!value || 'Required.',
        value => (value && value.length >= 3) || 'Min 3 characters',
      ],
    }),
  }
</script>