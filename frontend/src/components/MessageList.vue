<script setup>
import { ref } from "vue";
const props = defineProps(["userId"]);
const messages = ref(null);
messages.value = [];
let source = new EventSource(
  `http://localhost:5000/stream?channel=${props.userId}`,
);
source.addEventListener("message", function (event) {
  let data = JSON.parse(event.data);
  console.log(data.message);
  messages.value.push(data.message);
});
</script>

<template>
  <v-container>
    <v-list>
      <v-list-item v-for="(message, index) in messages">
        <v-divider v-if="index != 0"></v-divider>
        <v-list-item-title v-if="message.type === 'validado'">
          {{
            "[LANCE] ID Leilao: " +
            message.id_leilao +
            " - Usuário: " +
            message.id_user +
            " - Valor: " +
            message.valor_lance
          }}
        </v-list-item-title>
        <v-list-item-title v-else-if="message.type === 'invalidado'">
          {{
            "[LANCE INVALIDO] ID Leilao: " +
            message.id_leilao +
            " - Usuário: " +
            message.id_user +
            " - Valor: " +
            message.valor_lance
          }}
        </v-list-item-title>
        <v-list-item-title v-else-if="message.type === 'vencedor'">
          {{
            "[VENCEDOR] ID Leilao: " +
            message.id_leilao +
            " - Usuário: " +
            message.id_user_vencedor +
            " - Valor: " +
            message.valor_vencedor
          }}
        </v-list-item-title>
        <v-list-item-title v-else-if="message.type === 'link_pagamento'">
          {{
            "[LINK PAGAMENTO] ID Leilao: " +
            message.id_leilao +
            " - Link pagamento: " +
            message.payment_link +
            " - Valor: " +
            message.currency +
            " " +
            message.amount
          }}
        </v-list-item-title>
        <v-list-item-title v-else-if="message.type === 'status_pagamento'">
          {{
            "[STATUS PAGAMENTO] ID Leilao: " +
            message.id_leilao +
            " - Usuário: " +
            message.id_user +
            " - Valor: " +
            message.amount +
            " - Status: " +
            message.status
          }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<style scoped></style>
