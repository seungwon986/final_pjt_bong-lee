<template>
  <div class="container mb-4">
    <section class="recommendations">
      <h2 class="mb-4">도서 목록</h2>
      <p class="subtitle">마음에 드는 책을 북마크 해보세요 !</p>


      <!-- 도서목록 카테고리 -->
      <div class="tabs-wrapper bg-2">
        <RouterLink
          :to="{ name: 'books', query: { category: '전체' } }"
          class="tab-btn button button--aylen"
          :class="{ active: activeGenre === '전체' }"
        >
          전체
        </RouterLink>
        <RouterLink
          v-for="g in genres"
          :key="g"
          :to="{ name: 'books', query: { category: g } }"
          class="tab-btn button button--aylen button--border-thin button--round-s"
          :class="{ active: activeGenre === g }"
        >{{ g }}
        </RouterLink>
      </div>


       <!-- 도서목록 -->
      <div class="book-grid">
        <!-- 개별 도서목록 -->
        <div
          class="book-item"
          v-for="book in filteredBooks"
          :key="book.id"
        >
          <div class="cover">
            <img :src="book.cover" :alt="book.title" />
          </div>

          <div class="info">
            <div class="text">
              <div class="title">{{ book.title }}</div>
              <div class="author">{{ book.author }}</div>
              <div class="publisher">{{ book.publisher }}</div>
            </div>
            <label class="heart-label">
              <input type="checkbox" class="heart-checkbox">
              <svg class="icon" viewBox="0 0 1024 1024">
                <path class="heart-path"
                d="M742.4 101.12A249.6 249.6 0 0 0 512 256a249.6
                249.6 0 0 0-230.72-154.88C143.68
                101.12 32 238.4 32 376.32c0
                301.44 416 546.56 480 546.56s480-245.12
                480-546.56c0-137.92-111.68-275.2-249.6-275.2z"/>
              </svg>
              <span class="burst"></span>
            </label>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const books = ref([])
const activeGenre = ref('전체')
const route = useRoute()

onMounted(() => {
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

watch(
  () => route.query.category,
  (newCategory) => {
    activeGenre.value = newCategory || '전체'
  },
  { immediate: true }
)
</script>




<style scoped>
:root {
  --primary: #ff6b81;
  --gap: 16px;
}
body {
  font-family: 'Pretendard Variable', sans-serif;
  background: #fafafa;
  color: #333;
}
button { font-family: inherit; cursor: pointer; border: none; background: none; }
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;

}
h2 {
  font-weight: 500;
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 16px;
}

.subtitle {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 32px;
  text-align: center;
}

/* 책 카테고리 탭 */
.tabs-wrapper {
  width: 100%;
  text-align: center;
  padding-bottom: 100px;
   margin: 10px;
}

.tabs {
  display: inline-flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 20px;
}

.tab-btn,
a .tab-btn {
  position: relative;
  overflow: hidden;
  margin-right: 12px; 
  font-size: 0.8rem;
  border-radius: 6px;
  color: #333;
  cursor: pointer;
  background: #fff;
  transition: color 0.3s;
  border: none;
  padding: 0.3rem 1.1rem;
  text-align: center;
  text-decoration: none;
  display: inline-block;
}
.tab-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(126, 130, 194, 0.11);
}
.tab-btn.active {
  background: var(--primary);
  color: #e93b6f;
    font-weight: 600;
}




/* Aylen */
.button.button--aylen {
  padding: 0.3rem 1.1rem;
  gap: 12px;
  background: #fff;
  color: #37474f;
  overflow: hidden;
  -webkit-transition: color 0.3s;
  transition: color 0.3s;
}
.button--aylen.button--inverted {
  background: none;
  color: #fff;
}
.button--aylen::before,
.button--aylen::after {
  content: '';
  position: absolute;
  height: 100%;
  width: 100%;
  bottom: 100%;
  left: 0;
  z-index: -1;
  -webkit-transition: -webkit-transform 0.3s;
  transition: transform 0.3s;
  -webkit-transition-timing-function: cubic-bezier(0.75, 0, 0.125, 1);
  transition-timing-function: cubic-bezier(0.75, 0, 0.125, 1);
}
.button--aylen::before {
  background: #ff74d1;
}
.button--aylen::after {
  background: #ff65cc;
}
.button--aylen:hover {
  color: #fff;
}
.button--aylen:hover::before,
.button--aylen:hover::after {
  -webkit-transform: translate3d(0, 100%, 0);
  transform: translate3d(0, 100%, 0);
}
.button--aylen:hover::after {
  -webkit-transition-delay: 0.175s;
  transition-delay: 0.175s;
}



.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 30px;
  padding: 40px 20px;
  justify-content: center; 
}

.book-item {
  margin: 0 auto;
  max-width: 140px;
  position: relative;
  flex: 0 0 180px;
  width: 100%;
  overflow: visible;    
  background: transparent;
  border: none;
  transition: transform 0.2s ease;
  flex-shrink: 0; /* 추가: 줄어들지 않도록 고정 */
}
.book-item:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}
.cover {
  width: 100%;
  height: 240px;
  overflow: visible;     /* 이미지도 잘리지 않게 */
  transition: transform .2s;
}
.cover img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.cover:hover {
transform: translateY(-3px);
}
.info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  height: 130px;
}
.text {
  display: flex;
  flex-direction: column;
  gap: 1px;
  flex-grow: 1;
}
.title {
  font-size: 0.9rem;
  font-weight: bold;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 2줄까지만 표시 */
  height: calc(1.5em * 2); /* 2줄 높이 고정 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5;
}
.author {
  font-size: 0.8rem;
  color: #666;
  -webkit-line-clamp: 1; /* 2줄까지만 표시 */
  height: calc(1.3em * 1); /* 2줄 높이 고정 */
  overflow: hidden;
    text-overflow: ellipsis;
}
.publisher {
  font-size: 0.75rem;
  color: #889c18;
  -webkit-line-clamp: 1; /* 2줄까지만 표시 */
  height: calc(1.3em * 1); /* 2줄 높이 고정 */
  overflow: hidden;
    text-overflow: ellipsis;
}
@media (max-width: 1200px) {
  .book-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}
@media (max-width: 992px) {
  .book-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
@media (max-width: 768px) {
  .book-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 576px) {
  .book-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}


/* 북마크 하트 효과 */
.heart-label {
  position: absolute; 
  margin-left: auto;      /* 왼쪽 여백을 최대화해 오른쪽 정렬 */
  width: 24px; height: 24px;
  cursor: pointer;

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
  stroke: #ff9d9d;
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
    0 -40px 0 var(--primary),
    0 40px 0 var(--primary),
    -40px 0 0 var(--primary),
    40px 0 0 var(--primary),
    -30px -30px 0 var(--primary),
    30px -30px 0 var(--primary),
    30px 30px 0 var(--primary),
    -30px 30px 0 var(--primary);
  opacity: 0;
}
/* 체크 시 애니메이션 */
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
      0%   { stroke-dashoffset: 300; fill: #eee; }
      80%  { stroke-dashoffset:   0; fill: #eee; }
      100% { stroke-dashoffset:   0; fill: var(--primary); }
    }
    @keyframes beat {
      0%,70% { transform: scale(1); }
      80%    { transform: scale(1.2); }
      100%   { transform: scale(1); }
    }
    @keyframes blink {
      0%   { transform: translate(-50%,-50%) scale(0.5); opacity:0.8; }
      80%  { transform: translate(-50%,-50%) scale(1);   opacity:1;   }
      100% { transform: translate(-50%,-50%) scale(1.1); opacity:0;   }
    }
</style>