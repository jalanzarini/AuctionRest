<script setup>
import { ref } from 'vue';
const auctions = ref(null);

auctions.value = [
     {
         title: 'Auction',
         subscribed: false,
     },
     {
         title: 'Auction',
         subscribed: false,
     },
     {
         title: 'Auction',
         subscribed: false,
     },
     {
         title: 'Auction',
         subscribed: true,
     },
     {
         title: 'Auction',
         subscribed: false,
     },
 ];

 function subscribe(index){

 }

 function unsubscribe(index){

 }
</script>

<template>
  <v-container overflow>
    <v-list>
      <template v-for="(auction, index) in auctions">
        <v-divider v-if="index != 0"></v-divider>
        <v-list-item>
            <template v-slot:append>
                <v-btn v-if='auction.subscribed' @click="subscribe(index)">Subscribe</v-btn>
                <v-btn v-else @click='unsubscribe(index)'>Unsubscribe</v-btn>
            </template>
            <template v-slot:default>{{ auction.title}}</template>
        </v-list-item>
      </template>
    </v-list>
  </v-container>
</template>

<style scoped>
</style>
