<template>
  <div class="container mt-4">
    <h2 class="mb-3">📚 나의 선호도 기반 도서 목록</h2>
    <div v-if="books.length" class="row row-cols-1 row-cols-md-3 g-4">
      <BookCard
        v-for="book in books"
        :key="book.id"
        :book="book"
      />
    </div>
    <div v-else>
      <p>최근에 관심 가지고 고른 도서 기반으로 추천 도서를 조회합니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import BookCard from '../BookCard.vue'
import { useAccountStore } from '@/stores/accounts.js'

const books = ref([])
const store = useAccountStore()

const fetchRecommend = async () => {
  if (!store.user?.preferred_books?.length) return

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/v1/books/recommend/', {
      preferred_books: store.user.preferred_books
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })
    books.value = res.data
  } catch (err) {
    console.error('추천 도서 불러오기 실패:', err.response?.data || err.message)
  }
}

watch(() => store.user?.preferred_books, () => {
  fetchRecommend()
}, { immediate: true })
</script>
