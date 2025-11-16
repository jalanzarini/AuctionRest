<script setup>
const messages = [
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
  {
    auction: {
      name: "Leilão 1",
    },
    message: "Novo lance: 50",
  },
]
</script>

<template>
    <v-container>
        <v-list>
            <v-list-item v-for="(message, index) in messages">
                <v-divider v-if="index != 0"></v-divider>
                <v-list-item-title>{{ message.auction.name + " " + message.message }}</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-container>
</template>

<style scoped>
</style>
