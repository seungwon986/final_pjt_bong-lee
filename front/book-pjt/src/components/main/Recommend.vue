<template>
  <div>
    <h3 class="section-title">나의 선호도 기반 추천 도서</h3>
    <p class="sub">내가 선호하는 책과 비슷한 책을 추천 받아보세요 !</p>
    <div class="recommend-section">
      <div v-if="books.length">
        <div class="slider-wrapper">
          <button class="slide-btn left" @click="slideLeft">‹</button>
  
          <div class="book-slider" ref="slider">
            <div
  class="book-card"
  v-for="book in books"
  :key="book.id"
  @click="goToDetail(book.id)"
>
              <img :src="book.cover" :alt="book.title" class="book-cover" />
              <p class="book-title">{{ book.title }}</p>
            </div>
          </div>
  
          <button class="slide-btn right" @click="slideRight">›</button>
        </div>
      </div>
  
      <div v-else class="empty-message">
        📌 최근 관심 도서를 기반으로 추천 결과를 가져오는 중입니다.
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const books = ref([])
const store = useAccountStore()
const slider = ref(null)

// 상세페이지 이동 함수 
const goToDetail = (bookId) => {
  router.push(`/books/${bookId}`)
}
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
    console.error('❌ 추천 도서 불러오기 실패:', err.response?.data || err.message)
  }
}

const slideLeft = () => {
  slider.value.scrollLeft -= 400
}

const slideRight = () => {
  slider.value.scrollLeft += 400
}

watch(
  () => store.user?.preferred_books,
  () => fetchRecommend(),
  { immediate: true }
)
</script>

<style scoped>
.sub {
  padding-left: 20px;
}
.recommend-section {
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1rem;
  background-color: #fae4c780;
  border-radius: 16px;
}
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: left;
  margin-bottom: 1.2rem;
  margin-left: 20px;
  color: #4e4e4e;
}

.slider-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.book-slider {
  display: flex;
  gap: 1.2rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0 5rem 3rem 5rem;
}

.book-card {
  cursor: pointer;
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

.empty-message {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1rem;
}
</style>
