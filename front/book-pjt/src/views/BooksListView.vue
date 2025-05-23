<template>
  <div class="container mt-4">
    <h2 class="mb-3">🌟 전체 도서 목록</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <BookCard
        v-for="book in books"
        :key="book.id"
        :book="book"
        :is-preferred="isPreferred(book.id)"
        @toggle-preferred="handleTogglePreferred"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BookCard from '@/components/BookCard.vue'
import { useAccountStore } from '@/stores/accounts.js'

const books = ref([])
const store = useAccountStore()

const fetchBooks = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/books/')
    books.value = res.data
  } catch (err) {
    console.error('도서 목록 불러오기 실패:', err.response?.data || err.message)
  }
}

const isPreferred = (bookId) => {
  return store.user?.preferred_books?.includes(bookId) ?? false
}

const handleTogglePreferred = async (bookId) => {
  try {
    const current = store.user?.preferred_books || []
    const updated = current.includes(bookId)
      ? current.filter(id => id !== bookId)
      : [...current, bookId]

    await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      preferred_books: updated
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })

    await store.fetchUserProfile()
  } catch (err) {
    console.error('선호도 변경 실패:', err.response?.data || err.message)
  }
}

onMounted(() => {
  fetchBooks()
  if (store.isLogIn && !store.user) {
    store.fetchUserProfile()
  }
})
</script>
