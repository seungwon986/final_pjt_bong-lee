<template>
  <div>
    <nav class="navbar navbar-expand navbar-dark bg-dark px-3">
      <RouterLink class="navbar-brand" to="/">BookApp</RouterLink>
      <RouterLink
        v-if="!store.isLogIn"
        class="navbar-brand"
        :to="{ name: 'SignUpView' }"
        >SIGNUP</RouterLink
      >
      <RouterLink
        v-if="!store.isLogIn"
        class="navbar-brand"
        :to="{ name: 'LogInView' }"
        >LOGIN</RouterLink
      >
      <form @submit.prevent="logOut" v-if="store.isLogIn" class="ms-2">
        <button type="submit" class="btn btn-outline-light">LOGOUT</button>
      </form>
      <ul class="navbar-nav">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/books">도서 목록</RouterLink>
        </li>
      </ul>
    </nav>

    <main class="container py-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/accounts.js";
import { onMounted } from 'vue'
import axios from 'axios'

const store = useAccountStore();
const logOut = function () {
  store.LogOut();
};
onMounted(() => {
  axios.post('http://127.0.0.1:8000/api/v1/books/import/')
    .then(res => {
      console.log(res.data.message || '책 불러오기 완료')
    })
    .catch(err => {
      console.error('책 불러오기 실패:', err)
    })
})
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
}
</style>
