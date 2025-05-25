<template>
  <div class="container py-4">
    <h2 class="mb-4">📝 챌린지 생성</h2>

    <form @submit.prevent="createChallenge" class="border p-3 rounded shadow-sm">
      <div class="mb-2">
        <input v-model="form.title" type="text" class="form-control" placeholder="챌린지 제목" required />
      </div>
      <div class="mb-2">
        <textarea v-model="form.description" class="form-control" placeholder="챌린지 설명" rows="2"></textarea>
      </div>
      <div class="row mb-2">
        <div class="col">
          <input v-model="form.start_date" type="date" class="form-control" required />
        </div>
        <div class="col">
          <input v-model="form.end_date" type="date" class="form-control" required />
        </div>
        <div class="col">
          <input v-model.number="form.target_books" type="number" class="form-control" placeholder="목표 권수" required />
        </div>
      </div>
      <button type="submit" class="btn btn-success">생성 완료</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const store = useAccountStore()
const router = useRouter()
const API_URL = 'http://127.0.0.1:8000/api/v1'

const form = ref({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  target_books: 1,
})

const createChallenge = () => {
  axios.post(`${API_URL}/challenges/`, form.value, {
    headers: {
      Authorization: `Token ${store.token}`,
    }
  })
    .then(() => {
      router.push('/challenges')
    })
    .catch(err => console.error(err))
}
</script>
