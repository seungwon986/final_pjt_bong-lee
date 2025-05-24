<template>
  <div class="challenge-list">
    <ChallengeItem
      v-for="challenge in challenges"
      :key="challenge.id"
      :challenge="challenge"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ChallengeItem from '@/components/main/ChallengeItem.vue'

const challenges = ref([])

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/challenges/')
    .then(res => {
      challenges.value = res.data
    })
    .catch(err => {
      console.error('챌린지 불러오기 실패:', err)
    })
})
</script>

<style scoped>
.challenge-list {
  display: grid;
  gap: 1.5rem;
}
</style>
