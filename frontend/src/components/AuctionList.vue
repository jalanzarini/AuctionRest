<script setup>
import { ref } from "vue";
const props = defineProps(["userId"]);
const auctions = ref(null);

updateList();

async function updateList() {
  const response = await fetch("http://localhost:5000/auction/consult", {
    method: "GET",
  });
  auctions.value = await response.json();
}

function subscribe(index) {
  const data = {
    id_leilao: index,
    id_user: props.userId,
  };

  fetch("http://localhost:5000/auction/interest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

function unsubscribe(index) {
  const data = {
    id_leilao: index,
    id_user: props.userId,
  };

  fetch("http://localhost:5000/auction/uninterest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}
</script>

<template>
  <v-container overflow>
    <v-list>
      <template v-for="(auction, index) in auctions">
        <v-divider v-if="index != 0"></v-divider>
        <v-list-item>
          <template v-slot:append>
            <v-btn @click="subscribe(auction.id)">SUB</v-btn>
            <v-btn class="mr-1" @click="unsubscribe(auction.id)">UNSUB</v-btn>
          </template>
          <template v-slot:default>
            {{ "ID: " + auction.id + " - " + auction.nome }}
          </template>
        </v-list-item>
      </template>
    </v-list>
    <v-btn @click="updateList">Refresh List</v-btn>
  </v-container>
</template>

<style scoped></style>
