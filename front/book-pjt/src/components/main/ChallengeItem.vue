<!-- components/main/ChallengeItem.vue -->
<template>
  <div class="challenge-card">
    <h3>{{ challenge.title }}</h3>
    <p>{{ challenge.description }}</p>
    <p class="date">📅 {{ challenge.start_date }} ~ {{ challenge.end_date }}</p>
  </div>
</template>

<script setup>
defineProps({
  challenge: Object
})
</script>

<style scoped>
.challenge-card {
  padding: 1.2rem;
  border-radius: 10px;
  background-color: #fff6fb;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

.date {
  font-size: 0.875rem;
  color: #777;
}
</style>
