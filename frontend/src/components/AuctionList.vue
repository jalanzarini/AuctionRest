<script setup>
import { ref } from 'vue';
const auctions = ref(null);

auctions.value = [
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
  {nome: "L1"},
]

</script>

<template>
  <v-container overflow>
    <v-list>
      <template v-for="auction in auctions">
        <v-divider></v-divider>
        <v-list-item {{ auction.nome }}></v-list-item>
      </template>
    </v-list>
  </v-container>
</template>

<style scoped>
</style>
