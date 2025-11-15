<script setup>
import { ref } from 'vue';
import DatePicker from './DatePicker.vue';
import TimePicker from './TimePicker.vue';
const name = ref(null);
const description = ref(null);
const startDate = ref(new Date());
const startTime = ref(startDate.value.getHours()+":"+startDate.value.getMinutes());
const endDate = ref(new Date());
const endTime = ref(endDate.value.getHours()+":"+endDate.value.getMinutes());

function formatDate(date, time){
  return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()} ${time}:00`;
}

function createAuction(){    
  let data = {
    name: name.value,
    description: description.value,
    startDateTime: formatDate(startDate.value, startTime.value),
    endDateTime: formatDate(endDate.value, endTime.value),
  };

  console.log(data);

  fetch("teste.com", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
}
</script>

<template>
  <v-container class="d-flex flex-column justify-space-between">
    <v-form>
      <v-text-field label="Name" v-model="name"></v-text-field>
      <v-text-field label="Description" v-model="description"></v-text-field>
      <DatePicker label="Start Date" v-model="startDate"></DatePicker>
      <TimePicker label="Start Time" v-model="startTime"></TimePicker>
      <DatePicker label="End Date" v-model="endDate"></DatePicker>
      <TimePicker label="End Time" v-model="endTime"></TimePicker>
    </v-form>
    <v-row class="d-flex justify-end">
      <v-btn @click="createAuction">Create</v-btn>
    </v-row>
  </v-container>
</template>

<style scoped>
</style>
