<template>
  <div class="bestseller-section">
    <h2 class="section-title">베스트셀러</h2>

    <div class="category-tabs">
      <button
        v-for="g in genres"
        :key="g"
        :class="{ active: activeGenre === g }"
        @click="filterByCategory(g)"
      >{{ g }}</button>
    </div>

    <div class="slider-wrapper">
      <button class="slide-btn left" @click="slideLeft">‹</button>

      <div class="book-slider" ref="slider">
        <div class="book-card" v-for="book in filteredBooks" :key="book.id">
          <img :src="book.cover" :alt="book.title" class="book-cover" />
          <p class="book-title">{{ book.title }}</p>
        </div>
      </div>

      <button class="slide-btn right" @click="slideRight">›</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const books = ref([])
const genres = ref([])
const activeGenre = ref('전체')
const slider = ref(null)

const filteredBooks = computed(() => {
  if (activeGenre.value === '전체') return books.value
  return books.value.filter(b => b.category?.name === activeGenre.value)
})

const filterByCategory = (genre) => {
  activeGenre.value = genre
}

const slideLeft = () => {
  slider.value.scrollLeft -= 400
}

const slideRight = () => {
  slider.value.scrollLeft += 400
}

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then(res => {
      books.value = res.data
      genres.value = ['전체', ...new Set(res.data.map(b => b.category?.name).filter(Boolean))]
    })
})
</script>



<style scoped>
.bestseller-section {
  width: 100%;
  
  margin: 0 auto;
  padding: 2rem 1rem;
  background-color: #f8f9fb; /* 은은한 배경색 */
  border-radius: 16px;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 500;
  text-align: left;
  margin-bottom: 1.2rem;
  margin-left: 30px;
  color: #333;
}

/* 카테고리 탭 버튼 */
.category-tabs {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 1.5rem;
}

.category-tabs button {
  padding: 0.3rem 0.8rem;
  font-size: 0.85rem;
  border: 1px solid #ccc;
  border-radius: 999px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.category-tabs button.active,
.category-tabs button:hover {
  background-color: #4ef748;
  color: white;
  font-weight: bold;
}

/* 슬라이더 구조 */
.slider-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* 카드 슬라이더 내부 */
.book-slider {
  display: flex;
  gap: 1.2rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0 5rem 3rem 5rem;
}

/* 각 책 카드 스타일 */
.book-card {
  min-width: 150px;
  max-width: 150px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 0.8rem;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  flex-shrink: 0;
}

.book-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
}

.book-cover {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
}

.book-title {
  margin-top: 0.6rem;
  font-size: 0.85rem;
  color: #333;
  font-weight: 500;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 슬라이드 버튼 */
.slide-btn {
  background: white;
  border: 1px solid #ccc;
  border-radius: 50%;
  font-size: 1.2rem;
  width: 32px;
  height: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.slide-btn.left {
  left: 0.3rem;
}

.slide-btn.right {
  right: 0.3rem;
}
</style>
