<!-- views/SignUpView.vue -->

<template>
  <div>
    <form @submit.prevent="onLogIn">
      <label for="username">Username: </label>
      <input type="text" id="username" v-model="username" />
      <br />
      <label for="password1">Password: </label>
      <input type="password" id="password" v-model="password" />
      <br />
      <input type="submit" value="로그인" />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/accounts.js";
const store = useAccountStore();
const username = ref("");
const password = ref("");

const onLogIn = function () {
  const info = {
    username: username.value,
    password: password.value,

  };
  store.logIn(info)
};
</script>

<style>
</style>
