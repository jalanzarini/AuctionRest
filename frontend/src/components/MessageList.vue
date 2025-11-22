<script setup>
import { ref } from "vue";
const props = defineProps(["userId"]);
const messages = ref(null);
let source = new EventSource(
  `http://localhost:5000/stream?channel=${props.userId}`,
);
source.addEventListener("message", function (event) {
  let data = JSON.parse(event.data);
  console.log(data.message);
  messages.append(data.message);
});
</script>

<template>
  <v-container>
    <v-list>
      <v-list-item v-for="(message, index) in messages">
        <v-divider v-if="index != 0"></v-divider>
        <v-list-item-title>
          {{ message.auction.name + " " + message.message }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<style scoped></style>
