<template>
  <v-row>
    <v-col>
      <v-sheet height="400">
        <v-calendar
          color="primary"
          type="day"
          data-label="calendar"
        >
          <template v-slot:day-header="{ present }">
            <template
              v-if="present"
            >
              Today
            </template>
          </template>

          <template v-slot:interval="{ hour }">
            <div
              class="text-center"
            >
              {{ hour }} o'clock
            </div>
          </template>
        </v-calendar>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
  export default {
    data: () => ({}),
  }
</script>