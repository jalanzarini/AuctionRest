<script setup>
import MessageList from './MessageList.vue';
import AuctionList from './AuctionList.vue';
import AuctionWizard from './AuctionWizard.vue';
</script>

<template>
  <layout class="rounded rounded-md border">
    <v-app-bar title="Front"></v-app-bar>
    <v-navigation-drawer width="500">
      <v-list nav>
        <v-list-item title="Auction Wizard"></v-list-item>
        <v-divider></v-divider>
        <AuctionWizard></AuctionWizard>
      </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer location="right" width="400">
      <v-list nav>
        <v-list-item title="Auction List"></v-list-item>
        <v-divider></v-divider>
        <AuctionList></AuctionList>
      </v-list>
    </v-navigation-drawer>

    <v-main class="d-flex align-center justify-center" height="300">
      <MessageList></MessageList>
    </v-main>
  </layout>
</template>

<style scoped>
</style>
