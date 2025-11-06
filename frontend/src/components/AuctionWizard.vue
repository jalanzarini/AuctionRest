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

function createAuction(){
  let [startHour, startMinute] = startTime.value.split(":");
  let startDateTime = startDate.value;
  startDateTime.setHours(startHour);
  startDateTime.setMinutes(startMinute);

  let [endHour, endMinute] = endTime.value.split(":");
  let endDateTime = endDate.value;
  endDateTime.setHours(endHour);
  endDateTime.setMinutes(endMinute);
  
  let data = {
    name: name.value,
    description: description.value,
    startDateTime: startDateTime,
    endDateTime: endDateTime,
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
  <v-container width="300">
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
