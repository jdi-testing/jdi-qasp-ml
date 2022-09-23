<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Regular"
            disabled
            data-label="text-field"
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Regular"
            readonly
            data-label="text-field"
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Solo"
            solo
            data-label="text-field"
            disabled
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Solo"
            solo
            readonly
            data-label="text-field"
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Filled"
            filled
            disabled
            data-label="text-field"
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Filled"
            filled
            readonly
            data-label="text-field"
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Outlined"
            outlined
            disabled
            data-label="text-field"
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          sm="6"
        >
          <v-text-field
            value="John Doe"
            label="Outlined"
            outlined
            readonly
            data-label="text-field"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>