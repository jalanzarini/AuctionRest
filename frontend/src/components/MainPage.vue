<script setup>
import MessageList from './MessageList.vue';
import AuctionList from './AuctionList.vue';
import AuctionWizard from './AuctionWizard.vue';
</script>

<template>
  <v-row>
    <v-col cols="3" class="d-flex justify-center align-center">
      <v-card title="Auction Wizard" variant="outlined">
        <AuctionWizard/>
      </v-card>
    </v-col>
    <v-col cols="3" class="d-flex justify-center align-center">
      <v-card title="Auction List" variant="outlined">
        <AuctionList/>
      </v-card>
    </v-col>
    <v-col cols="6" class="d-flex justify-center align-center">
        <v-card title="Message List" variant="outlined">
          <MessageList/>
        </v-card>
    </v-col>
  </v-row>
</template>

<style scoped>
</style>
