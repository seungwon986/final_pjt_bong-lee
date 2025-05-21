<template>
  <div>
    <nav class="navbar navbar-expand navbar-dark bg-dark px-3">
      <RouterLink class="navbar-brand" to="/">BookApp</RouterLink>

      <ul class="navbar-nav">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/books">📚 도서 목록</RouterLink>
        </li>
      </ul>
    </nav>

    <main class="container py-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
}
</style>
