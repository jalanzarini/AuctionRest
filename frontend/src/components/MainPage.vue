<script setup>
import MessageList from "./MessageList.vue";
import AuctionList from "./AuctionList.vue";
import AuctionWizard from "./AuctionWizard.vue";
import BidWizard from "./BidWizard.vue";
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="3">
        <h2>Auction List</h2>
        <Suspense>
          <AuctionList height="800" class="overflow-auto"></AuctionList>
        </Suspense>
      </v-col>
      <v-divider vertical></v-divider>
      <v-col cols="6">
        <h2>Messages</h2>
        <MessageList height="800" class="overflow-auto"></MessageList>
      </v-col>
      <v-divider vertical></v-divider>
      <v-col cols="3">
        <h2>Auction Wizard</h2>
        <AuctionWizard></AuctionWizard>
        <h2>Bid</h2>
        <BidWizard></BidWizard>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
