<script setup>
import { ref } from "vue";
import DatePicker from "./DatePicker.vue";
import TimePicker from "./TimePicker.vue";
const name = ref(null);
const description = ref(null);
const startValue = ref(null);
const startDate = ref(new Date());
const startTime = ref(
  startDate.value.getHours() + ":" + startDate.value.getMinutes(),
);
const endDate = ref(new Date());
const endTime = ref(
  endDate.value.getHours() + ":" + endDate.value.getMinutes(),
);

function formatDate(date, time) {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${time}:00`;
}

function createAuction() {
  let data = {
    nome: name.value,
    descricao: description.value,
    valor_inicial: startValue.value,
    data_hora_inicio: formatDate(startDate.value, startTime.value),
    data_hora_fim: formatDate(endDate.value, endTime.value),
  };

  console.log(data);

  fetch("http://localhost:5000/auction/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}
</script>

<template>
  <v-container class="d-flex flex-column justify-space-between">
    <v-form>
      <v-text-field label="Name" v-model="name"></v-text-field>
      <v-text-field label="Description" v-model="description"></v-text-field>
      <v-number-input label="Start Value" v-model="startValue"></v-number-input>
      <v-row class="mx-1">
        <DatePicker label="Start Date" v-model="startDate"></DatePicker>
        <TimePicker label="Start Time" v-model="startTime"></TimePicker>
      </v-row>
      <v-row class="mx-1">
        <DatePicker label="End Date" v-model="endDate"></DatePicker>
        <TimePicker label="End Time" v-model="endTime"></TimePicker>
      </v-row>
    </v-form>
    <v-row class="mt-3 d-flex justify-end">
      <v-btn @click="createAuction">Create</v-btn>
    </v-row>
  </v-container>
</template>

<style scoped></style>
