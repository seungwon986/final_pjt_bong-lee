<template>
    <div class="main-container">

      <div class="best-container">
        <BestSeller />
      </div>
    
       <div class="row-section">
      <!-- 챌린지 -->
      <div class="half-section challenge-box">
        <h2 class="section-title">📢 진행 중인 챌린지</h2>
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

      <!-- 커뮤니티 -->
      <div class="half-section community-box">
        <h2 class="section-title">💬 커뮤니티</h2>
        <div class="slider-wrapper">
          <button class="slide-btn left" @click="slideLeftCommunity">‹</button>
          <div class="slider" ref="communitySlider">
            <div class="card" v-for="post in posts" :key="post.id">
              <h4 class="title">{{ post.title }}</h4>
              <p class="intro">{{ post.preview }}</p>
            </div>
          </div>
          <button class="slide-btn right" @click="slideRightCommunity">›</button>
        </div>
        <RouterLink to="/community" class="more-link">→ 더 보기</RouterLink>
      </div>
    </div>
    </div>
    
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
// import HeroSection from '@/components/main/HeroSection.vue'
// import CategoryButtons from '@/components/main/CategoryButtons.vue'
import BestSeller from '@/components/main/BestSeller.vue'



const challenges = ref([])

const slider = ref(null)

const slideLeft = () => {
  slider.value.scrollLeft -= 400
}
const slideRight = () => {
  slider.value.scrollLeft += 400
}
onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/challenges/')
    .then(res => {
      challenges.value = res.data
    })
    .catch(err => {
      console.error('챌린지 불러오기 실패:', err)
    })
})
</script>

<style scoped>
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* 베스트셀러와 row-section 간 간격 */
.best-container {
  margin-bottom: 3rem;
}

/* 챌린지/커뮤니티 반반 박스 */
.row-section {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  flex-wrap: wrap;
}

/* 각 박스 너비 */
.half-section {
  flex: 1 1 0;
  background-color: #f6f8fa;
  border-radius: 16px;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  min-width: 300px;
}

/* 기존에 있던 클래스 - 수정 금지 */
.section-title {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 1.2rem;
  text-align: left;
}

/* 슬라이더 영역 */
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

/* 카드 스타일 */
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

.title {
  font-weight: bold;
  font-size: 0.95rem;
  margin-bottom: 0.4rem;
}

.intro {
  font-size: 0.8rem;
  color: #666;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 더보기 버튼 */
.more-link {
  display: block;
  text-align: right;
  margin-top: 1rem;
  color: #fc47b0;
  font-weight: bold;
  font-size: 0.9rem;
  text-decoration: none;
}

/* 슬라이드 버튼 */
.slide-btn {
  background: white;
  border: 1px solid #ccc;
  border-radius: 50%;
  font-size: 1.2rem;
  width: 28px;
  height: 28px;
  display: flex;
  justify-content: center;
  align-items: center;
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

/* 반응형 처리 */
@media (max-width: 960px) {
  .row-section {
    flex-direction: column;
  }

  .half-section {
    width: 100%;
  }
}


</style>
