<template>
  <div class="challenge-list-view">
    <h1>챌린지 목록</h1>
    <ChallengeList />
  </div>
</template>

<script setup>
import ChallengeList from '@/components/challenge/ChallengeList.vue'
</script>

<style scoped>
.challenge-list-view {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

h1 {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}
</style>
