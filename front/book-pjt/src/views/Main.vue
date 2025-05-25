<template>
  <div class="main-wrapper">
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
        <!-- 추천 도서 & 베스트셀러 -->
        <div class="row-section section-observe">
          <Recommend />
          <BestSeller :books="bestSellers" />
        </div>

        <!-- 진행 중인 챌린지 -->
        <div class="row-section">
          <div class="half-section challenge-box section-observe" ref="challengeSection">
            <h2 class="section-title">💪 진행 중인 챌린지</h2>
            <div class="slider-wrapper">
              <button class="slide-btn left" @click="slideLeftChallenge">‹</button>
              <div class="slider" ref="challengeSlider">
                <div class="card" v-for="c in challenges" :key="c.id">
                  <h4 class="title">{{ c.title }}</h4>
                  <p class="intro">{{ c.intro }}</p>
                </div>
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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

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

const bestSellers = ref([])
const challenges = ref([])

const slideLeftChallenge = () => {
  const s = document.querySelector('.challenge-box .slider')
  if (s) s.scrollLeft -= 400
}

const slideRightChallenge = () => {
  const s = document.querySelector('.challenge-box .slider')
  if (s) s.scrollLeft += 400
}

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/bestsellers/')
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
</script>

<style scoped>
.hero-swiper {
  width: 100%;
  overflow: hidden;
}
.hero-image {
  width: 100% !important;
  height: auto !important;
  object-fit: cover;
}

.main-wrapper { width: 100%; }
.below-hero-bg {
  position: relative;
  background-color: #f7ffd593;
  padding-top: 3rem;
}
.below-hero-bg::before,
.below-hero-bg::after {
  content: '';
  position: absolute;
  top: 0;
  height: 100%;
  width: 1px;
  background: #ddd;
}
.below-hero-bg::before {
  left: calc((100% - min(100%, 1400px)) / 2);
}
.below-hero-bg::after {
  right: calc((100% - min(100%, 1400px)) / 2);
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
}
.row-section::after {
  content: '';
  display: block;
  height: 1px;
  background: #ddd;
  width: 100%;
  margin: 2rem 0 0;
}

.half-section {
  flex: 1 1 0;
  min-width: 300px;
  background-color: #abffdf56;
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
.slide-btn.left { left: 0.3rem; }
.slide-btn.right { right: 0.3rem; }

.section-observe {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s ease;
}
.section-observe.show {
  opacity: 1;
  transform: translateY(0);
}
</style>