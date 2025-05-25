<template>
  <div class="container py-4">
    <h2 class="mb-4">📘 챌린지 목록</h2>

    <!-- 챌린지 목록 -->
    <div v-if="challenges.length">
      <div v-for="challenge in challenges" :key="challenge.id" class="card mb-3 shadow-sm">
        <div class="card-body">
          <!-- 👇 챌린지 제목 클릭 시 상세 페이지로 이동 -->
          <RouterLink :to="`/challenges/${challenge.id}`" class="text-decoration-none text-dark">
            <h5 class="card-title">{{ challenge.title }}</h5>
          </RouterLink>
          <h6 class="card-subtitle text-muted">작성자: {{ challenge.creator_username }}</h6>
          <p class="card-text mt-2">{{ challenge.description }}</p>
          <p class="text-secondary">
            기간: {{ challenge.start_date }} ~ {{ challenge.end_date }} / 목표: {{ challenge.target_books }}권
          </p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>아직 등록된 챌린지가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const store = useAccountStore()
const API_URL = 'http://127.0.0.1:8000/api/v1'

const challenges = ref([])
const newChallenge = ref({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  target_books: 1,
})

const fetchChallenges = () => {
  axios.get(`${API_URL}/challenges/`)
    .then(res => {
      challenges.value = res.data
    })
    .catch(err => console.error(err))
}

const createChallenge = () => {
  axios.post(`${API_URL}/challenges/`, newChallenge.value, {
    headers: {
      Authorization: `Token ${store.token}`,
    }
  })
    .then(res => {
      challenges.value.unshift(res.data)
      newChallenge.value = { title: '', description: '', start_date: '', end_date: '', target_books: 1 }
    })
    .catch(err => console.error(err))
}

onMounted(fetchChallenges)
</script>

<style scoped>
.card-title {
  font-weight: 600;
}
</style>
