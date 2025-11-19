<script setup>
import { useDate } from "vuetify";
const adapter = useDate();
const props = defineProps(["label"]);
const time = defineModel();
</script>

<template>
  <v-menu z-index="10" :close-on-content-click="false">
    <template v-slot:activator="{ props }">
      <v-text-field
        :model-value="time"
        :label="label"
        prepend-icon="mdi-clock-time-four-outline"
        readonly
        v-bind="props"
      ></v-text-field>
    </template>
    <v-time-picker v-model="time"></v-time-picker>
  </v-menu>
</template>

<style scoped></style>
