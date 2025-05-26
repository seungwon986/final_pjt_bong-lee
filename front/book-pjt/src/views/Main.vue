<template>
  <div class="main-wrapper">
    <div class="gradient-bg" :style="{ opacity: gradientOpacity }"></div>

    <!-- 🖼️ Hero Swiper Section -->
    <div class="hero-swiper section-observe">
      <Swiper
        :modules="modules"
        :pagination="{ clickable: true }"
        :autoplay="{ delay: 4000 }"
        loop
      >
        <SwiperSlide v-for="(slide, index) in slides" :key="index">
          <img :src="slide.src" :alt="slide.alt" class="hero-image" />
        </SwiperSlide>
      </Swiper>
    </div>







    <div class="below-hero-bg">
      <div class="main-container">

        <div class="row-section section-observe">
          <Recommend v-if="store.isLogIn" class="half-section" />
        </div>

        <div class="row-section section-observe">
          <BestSeller :books="bestSellers" class="full-section" />
        </div>
  
        <div class="row-section">
  <div class="half-section challenge-box section-observe" ref="challengeSection">
    <h2 class="section-title">진행 중인 챌린지</h2>
    <p class="sub">카테고리별로 진행 중인 챌린지를 살펴보세요</p>

    <!-- ✅ 카테고리 탭 -->
    <div class="category-tabs">
      <button
        v-for="cat in categoryList"
        :key="cat"
        :class="{ active: cat === activeCategory }"
        @click="activeCategory = cat"
      >{{ cat }}</button>
    </div>

    <!-- ✅ 필터된 챌린지 슬라이드 -->
    <div class="slider-wrapper">
      <button class="slide-btn left" @click="slideLeftChallenge">‹</button>
      <div class="slider" ref="challengeSlider">
        <ChallengeItem
          v-for="c in filteredChallenges"
          :key="c.id"
          :challenge="c"
        />
      </div>
      <button class="slide-btn right" @click="slideRightChallenge">›</button>
    </div>

    <RouterLink to="/challenge/list" class="more-link">→ 더 보기</RouterLink>
  </div>
</div>

      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import { Pagination, Autoplay } from 'swiper/modules'

import BestSeller from '@/components/main/BestSeller.vue'
import Recommend from '@/components/main/Recommend.vue'

const modules = [Pagination, Autoplay]
const slides = [
  { src: '/img/bn1.png', alt: '배너1' },
  { src: '/img/bn2.png', alt: '배너2' },
]
const gradientOpacity = ref(0)
const bestSellers = ref([])
const challenges = ref([])
const store = useAccountStore()

const slideLeftChallenge = () => {
  const s = document.querySelector('.challenge-box .slider')
  if (s) s.scrollLeft -= 400
}
const slideRightChallenge = () => {
  const s = document.querySelector('.challenge-box .slider')
  if (s) s.scrollLeft += 400
}

onMounted(() => {
  axios.post('http://127.0.0.1:8000/api/v1/books/import/')
    .then(res => bestSellers.value = res.data)
    .catch(err => console.error('베스트셀러 로드 실패:', err))

  axios.get('http://127.0.0.1:8000/api/v1/challenges/')
    .then(res => challenges.value = res.data)
    .catch(err => console.error('챌린지 로드 실패:', err))

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      entry.target.classList.toggle('show', entry.isIntersecting)
    })
  }, { threshold: 0.15 })

  document.querySelectorAll('.section-observe').forEach(el => observer.observe(el))
})

import ChallengeItem from '@/components/main/ChallengeItem.vue'

const activeCategory = ref('전체')

const categoryList = computed(() => {
  const set = new Set(challenges.value.map(c => c.book?.category?.name).filter(Boolean))
  return ['전체', ...set]
})

const filteredChallenges = computed(() => {
  if (activeCategory.value === '전체') return challenges.value
  return challenges.value.filter(c => c.book?.category?.name === activeCategory.value)
})
</script>

<style scoped>
.main-wrapper {
  position: relative;
  width: 100%;
}
.sub {
  padding-left: 10px;
}
.gradient-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 200vh;
  background: linear-gradient(to bottom, #c5ffe9, #ffffff);
  z-index: -1;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.hero-swiper .swiper-slide img {
  width: 100%;
  object-fit: contain;
  max-height: 550px;
}

/* ② 파도 구분자 */
.wave-divider {
  width: 100%;
  overflow: hidden;
  line-height: 0;           /* 불필요한 여백 제거 */
  margin-top: -1px;         /* SVG 아래 선 겹침 방지 */
  position: relative;
  z-index: 2;
}
.wave-divider svg {
  display: block;
  width: 1400px;
  height: 50px;             /* 파도 높이 조절 가능 */
}

/* ③ 아래 섹션 배경색 */
.below-hero-bg {
  background-color: #b5f0bf6b; /* 원하는 파스텔 톤으로 변경 */
  position: relative;
  z-index: 1;
  padding: 60px 20px;       /* 위아래 여백 */
}
.below-hero-bg {
  position: relative;
  padding-top: 0.5rem;
}

.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
}

.row-section {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-top: 4rem;
  position: relative;
    background: #ffffffd8;
      border-radius: 16px;

}

.half-section {
  flex: 1 1 0;
  min-width: 300px;
  background: #ffffff9f;
  border-radius: 16px;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 1.2rem;
  padding-left: 10px;
}

.slider-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  margin-top: 0.5rem;
}

.slider {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0 0.5rem;
}
.slider::-webkit-scrollbar {
  display: none;
}

.card {
  min-width: 160px;
  max-width: 160px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 0.8rem;
  flex-shrink: 0;
  transition: transform 0.2s;
}
.card:hover {
  transform: translateY(-6px);
}

.more-link {
  display: block;
  text-align: right;
  margin-top: 1rem;
  color: #fc47b0;
  font-weight: bold;
  font-size: 0.9rem;
}

.slide-btn {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.slide-btn.left {
  left: 0.3rem;
}
.slide-btn.right {
  right: 0.3rem;
}

.section-observe {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s ease;
}
.section-observe.show {
  opacity: 1;
  transform: translateY(0);
}

.category-tabs {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.category-tabs button {
  padding: 0.4rem 1rem;
  border: none;
  border-radius: 2rem;
  background: #eaf8f0;
  color: #333;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s ease;
}
.category-tabs button.active {
  background: #2cd99c;
  color: #fff;
  font-weight: bold;
}
</style>
