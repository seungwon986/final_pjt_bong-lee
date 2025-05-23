<template>
  <div class="book-list-container">
    <div class="book-card" v-for="book in books" :key="book.id">
      <div class="bookmark-btn" @click="toggleBookmark(book)">
        <svg
          v-if="book.isBookmarked"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 24 24"
          class="bookmark-icon active"
        >
          <path d="M5 3c-.552 0-1 .448-1 1v17.382l7-3.11 7 3.11V4c0-.552-.448-1-1-1H5z" />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          class="bookmark-icon"
        >
          <path d="M5 3c-.552 0-1 .448-1 1v17.382l7-3.11 7 3.11V4c0-.552-.448-1-1-1H5z" />
        </svg>
      </div>
      <img :src="book.cover" :alt="book.title" class="book-cover" />
      <div class="book-info">
        <h3 class="book-title">{{ book.title }}</h3>
        <p class="book-author">👤 {{ book.author }}</p>
        <p class="book-publisher">🏢 {{ book.publisher }}</p>
        <p class="book-date">📅 {{ formattedDate(book.pub_date) }}</p>
        <p class="book-description">{{ book.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  books: Array,
})

function formattedDate(dateString) {
  return new Date(dateString).toLocaleDateString('ko-KR')
}

function toggleBookmark(book) {
  book.isBookmarked = !book.isBookmarked
}
</script>

<style scoped>
.book-list-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  padding: 40px;
  justify-content: center;
  max-width: 1200px;
  margin: auto;
}

.book-card {
  position: relative;
  background-color: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 0 0 transparent;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.book-card:hover {
  box-shadow: 0 20px 32px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.bookmark-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  cursor: pointer;
  z-index: 10;
}

.bookmark-icon {
  width: 24px;
  height: 24px;
  stroke: #bbb;
  transition: fill 0.3s, stroke 0.3s;
}

.bookmark-icon.active {
  fill: #ffc107;
  stroke: #ffc107;
}

.book-cover {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.book-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.book-title {
  font-size: 1.2rem;
  font-weight: bold;
}

.book-author,
.book-publisher,
.book-date,
.book-description {
  font-size: 0.9rem;
  color: #555;
}

.book-description {
  margin-top: 8px;
  line-height: 1.5;
  color: #666;
}
</style>