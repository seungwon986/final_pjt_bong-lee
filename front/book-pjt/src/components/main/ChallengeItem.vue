<template>
  <div class="challenge-card">

    <!-- ai로 이미지 생성하는 거.. -->
    <!-- <img :src="challenge.image_url || defaultImage" class="challenge-image" /> -->
    <h3>{{ challenge.title }}</h3>
    <p>{{ challenge.description }}</p>
    <p class="date">📅 {{ challenge.start_date }} ~ {{ challenge.end_date }}</p>

    <!-- 퍼센트 표시 -->
    <div class="progress-bar">
      <div class="progress" :style="{ width: progress + '%' }"></div>
    </div>
    <p class="progress-label">{{ progress }}%</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ challenge: Object })
const defaultImage = '/img/default-challenge.jpg'

const progress = computed(() => {
  const now = new Date()
  const start = new Date(props.challenge.start_date)
  const end = new Date(props.challenge.end_date)

  if (now < start) return 0
  if (now > end) return 100

  const total = end - start
  const elapsed = now - start
  return Math.floor((elapsed / total) * 100)
})
</script>

<style scoped>
.challenge-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.04);
  text-align: center;
}
.challenge-image {
  width: 100%;
  max-height: 160px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.75rem;
}
.progress-bar {
  height: 8px;
  width: 100%;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.5rem;
}
.progress {
  height: 100%;
  background-color: #2cd99c;
}
.progress-label {
  font-size: 0.75rem;
  margin-top: 0.25rem;
  color: #666;
}
.date {
  color: #888;
  font-size: 0.875rem;
}
</style>
