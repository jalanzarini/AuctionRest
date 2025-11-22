<script setup>
import { ref } from "vue";
const props = defineProps(["userId"]);
const auctionId = ref(null);
const value = ref(null);

function createBid() {
  let data = {
    id_leilao: auctionId.value,
    id_user: props.userId,
    valor_lance: value.value,
  };

  fetch("http://localhost:8000/bid/make", {
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
      <v-number-input label="Auction Id" v-model="auctionId"></v-number-input>
      <v-number-input label="Bid Amount" v-model="value"></v-number-input>
    </v-form>
    <v-row class="d-flex justify-end">
      <v-btn @click="createBid">Bid</v-btn>
    </v-row>
  </v-container>
</template>

<style scoped></style>
