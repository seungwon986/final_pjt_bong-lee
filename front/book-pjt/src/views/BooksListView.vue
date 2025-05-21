<template>
  <div class="container mt-4">
    <h2 class="mb-4">📚 베스트셀러 목록</h2>
    <div class="row">
      <div class="col-md-4 mb-4" v-for="book in books" :key="book.id">
        <BookCard :book="book" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BookCard from '@/components/BookCard.vue'

const books = ref([])

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then((res) => {
      books.value = res.data
    })
    .catch((err) => {
      console.error('책 불러오기 실패:', err)
    })
})
</script>
