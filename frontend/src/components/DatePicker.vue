<script setup>
import { useDate } from "vuetify";
const adapter = useDate();
const props = defineProps(["label"]);
const date = defineModel();
</script>

<template>
  <v-menu z-index="10" :close-on-content-click="false">
    <template v-slot:activator="{ props }">
      <v-text-field
        :model-value="adapter.format(date, 'fullDate')"
        :label="label"
        prepend-icon="mdi-calendar-blank"
        readonly
        v-bind="props"
      ></v-text-field>
    </template>
    <v-date-picker v-model="date"></v-date-picker>
  </v-menu>
</template>

<style scoped></style>
