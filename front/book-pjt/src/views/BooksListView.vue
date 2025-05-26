<template>
  <div class="book-list-container">
    <section class="recommendations">
      <div class="banner-images">
        <img
          src="/img/bookcat.png"
          alt="Book Catalog"
          class="banner-image"
        />
        
      </div>
    </section>
    <p class="subtitle">마음에 드는 책을 북마크 해보세요!</p>

    <div class="category-tabs">
      <RouterLink
        :to="{ name: 'books', query: { category: '전체' } }"
        class="category-tab"
        :class="{ active: activeGenre === '전체' }"
      >전체</RouterLink>
      <RouterLink
        v-for="g in genres"
        :key="g"
        :to="{ name: 'books', query: { category: g } }"
        class="category-tab"
        :class="{ active: activeGenre === g }"
      >{{ g }}</RouterLink>
    </div>

    <div class="book-grid">
      <div class="book-card" v-for="book in paginatedBooks" :key="book.id">
        <div class="book-card-inner">
          <img :src="book.cover" :alt="book.title" class="book-cover" />
          <div class="book-info">
            <div class="title-wrap">
              <h3 class="book-title clamp">{{ book.title }}</h3>
              <label class="heart-label">
                <input type="checkbox" :checked="isLiked(book.id)" @change="toggleBookmark(book.id)" class="heart-checkbox">
                <svg class="icon" viewBox="0 0 1024 1024">
                  <path class="heart-path"
                    d="M742.4 101.12A249.6 249.6 0 0 0 512 256a249.6
                    249.6 0 0 0-230.72-154.88C143.68
                    101.12 32 238.4 32 376.32c0
                    301.44 416 546.56 480 546.56s480-245.12
                    480-546.56c0-137.92-111.68-275.2-249.6-275.2z" />
                </svg>
                <span class="burst"></span>
              </label>
            </div>
            <p class="book-author">{{ book.author }}</p>
            <p class="book-publisher">{{ book.publisher }}</p>
            <p class="book-date">출판일 | {{ formattedDate(book.pub_date) }}</p>
            <p class="book-description">{{ book.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'

const store = useAccountStore()
const books = ref([])
const activeGenre = ref('전체')
const route = useRoute()
const currentPage = ref(1)
const itemsPerPage = 10

const likedBookIds = ref([])

onMounted(async () => {
  await store.fetchUserProfile()
  likedBookIds.value = store.user?.preferred_books || []

  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then(res => {
      books.value = res.data
    })
    .catch(err => {
      console.error('책 불러오기 실패:', err)
    })
})

const genres = computed(() => {
  const set = new Set(books.value.map(b => b.category?.name).filter(Boolean))
  return [...set]
})

const filteredBooks = computed(() => {
  if (activeGenre.value === '전체') return books.value
  return books.value.filter(b => b.category?.name === activeGenre.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredBooks.value.length / itemsPerPage)
})

const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredBooks.value.slice(start, end)
})

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

watch(
  () => route.query.category,
  (newCategory) => {
    activeGenre.value = newCategory || '전체'
    currentPage.value = 1
  },
  { immediate: true }
)

function formattedDate(dateString) {
  return new Date(dateString).toLocaleDateString('ko-KR')
}

function isLiked(bookId) {
  return likedBookIds.value.includes(bookId)
}

async function toggleBookmark(bookId) {
  const current = [...likedBookIds.value]
  const index = current.indexOf(bookId)
  if (index === -1) {
    current.push(bookId)
  } else {
    current.splice(index, 1)
  }
  likedBookIds.value = current

  try {
    await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      preferred_books: current
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })

    await store.fetchUserProfile()
  } catch (err) {
    console.error('북마크 저장 실패:', err)
  }
}
</script>


<style scoped>

.book-title.clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
.book-card,
.book-info,
.title-wrap {
  overflow: visible;
}
.recommendations {
  display: flex;
  align-items: center;
  height: 50vh;
  padding: 3rem 1rem;
}
.banner-title {
  font-size: 6rem;
  font-weight: 300;
  text-align: lefr;
  letter-spacing: -0.05em;
  margin-bottom: 0;
}
.banner-images {
  display: flex;

  align-items: center;
  gap: 0rem;
  padding: 3rem 1rem;
}
.banner-image {
  max-width: 100%;
  display: block;
}

.banner-subtitle {
  font-size: 3rem;
  font-weight: 300;
  text-align: center;
  margin-top: -0.5rem;
  padding-left: 10px;
  color: #333;
}
.book-list-container {
  max-width: 1400px; /* 기존 100% → 고정된 최대 너비로 변경 */
  margin: 0 auto;    /* 중앙 정렬 */
  padding: 0 1rem;
  background: #fff;
  font-family: 'AritaM', sans-serif;
}

.title-wrap {
  position: relative;
  padding-right: 36px; /* 하트 공간 확보 */
  overflow: visible;
}
.subtitle {
  padding-left: 30px;
  text-align: center;
  color: #888;
  margin-bottom: 2rem;
}
.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 2rem;
  padding-top: 50px;
  padding-bottom: 20px;
}
.category-tab {
  border: 1px solid #303331;
  border-radius: 20px;
  padding: 0.3rem 1rem;
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: none;
  color: #303030;
  transition: background 0.3s;
}
.category-tab.active,
.category-tab:hover {
  background: #4ef748;
  color: #fff;
}

/* 책 리스트 */
.book-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 한 줄에 2개 고정 */
  border-top: 1px solid #303030;
  border-left: 1px solid #303030;
}
.book-card {
  border-right: 1px solid #303030;
  border-bottom: 1px solid #303030;
  padding: 2rem;
  background-color: #fff;
  transition: box-shadow 0.2s ease; /* ✅ 여기만 transition */
  border-radius: 0;
}
.book-card-inner {
  display: flex;
  flex-direction: row;
  gap: 1.5rem;
  align-items: flex-start;
    border-radius: 1rem;

}
.book-card:hover {
   box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}
.heart-label {
  position: absolute;
  top: 0;
  right: 0;
  width: 24px;
  height: 24px;
  cursor: pointer;
    z-index: 10; /* 꼭 지정! */
      overflow: visible;
}
.heart-checkbox {
  display: none;
}
svg.icon {
  width: 24px;
  height: 24px;
  overflow: visible;
  animation: none;
}
.heart-path {
  fill: transparent;
  stroke: #ff99c8;
  stroke-width: 60px;
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  stroke-linecap: round;
}
.burst {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 8px;
  height: 8px;
  background: transparent;
  border-radius: 50%;
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0);
  box-shadow:
    0 -40px 0 #ff99c8,
    0 40px 0 #ff99c8,
    -40px 0 0 #ff99c8,
    40px 0 0 #ff99c8,
    -30px -30px 0 #ff99c8,
    30px -30px 0 #ff99c8,
    30px 30px 0 #ff99c8,
    -30px 30px 0 #ff99c8;
  opacity: 0;
}
.heart-checkbox:checked + svg.icon .heart-path {
  animation: drawHeart 0.8s linear forwards;
}
.heart-checkbox:checked + svg.icon {
  animation: beat 0.8s ease-in-out forwards;
}
.heart-checkbox:checked + svg.icon + .burst {
  animation: blink 0.6s ease-in-out forwards;
  animation-delay: 0.5s;
}
@keyframes drawHeart {
  0% { stroke-dashoffset: 300; fill: #eee; }
  80% { stroke-dashoffset: 0; fill: #eee; }
  100% { stroke-dashoffset: 0; fill: #ff99c8; }
}
@keyframes beat {
  0%,70% { transform: scale(1); }
  80% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
@keyframes blink {
  0% { transform: translate(-50%,-50%) scale(0.5); opacity:0.8; }
  80% { transform: translate(-50%,-50%) scale(1); opacity:1; }
  100% { transform: translate(-50%,-50%) scale(1.1); opacity:0; }
}
.book-card-inner {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}
.book-cover {
  width: 180px;
  height: auto;
  object-fit: contain;
  border-radius: 0.2rem;
  flex-shrink: 0;
cursor: pointer;
}
.book-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}
.book-title {
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: bold;
  line-height: 1.4;
}
.book-author,
.book-publisher,
.book-date {
  font-size: 0.9rem;
  color: #666;
}
.book-description {
  font-size: 0.9rem;
  color: #444;
  line-height: 1.5;
  margin-top: 0.5rem;

  display: -webkit-box;
  -webkit-line-clamp: 3; /* 최대 3줄까지만 보여줘 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}


/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 2rem 0;
  gap: 1rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.pagination button:hover:enabled {
  background-color: #e0e0e0;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination span {
  font-size: 0.95rem;
  color: #555;
}
</style>
