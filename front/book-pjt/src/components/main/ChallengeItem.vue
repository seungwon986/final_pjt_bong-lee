<template>
  <div class="challenge-item" :style="{ backgroundColor: backgroundColor }">
    <!-- 책 표지 -->
    <div class="cover-wrapper">
      <img :src="challenge.book.cover_image" :alt="challenge.book.title" />
    </div>

    <!-- 제목, 저자 -->
    <div class="content">
      <h3>{{ challenge.book.title }}</h3>
      <p>{{ challenge.book.author }}</p>
    </div>

    <!-- 기간 -->
    <p class="period">{{ formattedPeriod }}</p>

    <!-- 참여자 및 버튼 -->
    <div class="footer">
      <span>👥 {{ challenge.current_participants }} / {{ challenge.max_participants }}</span>
      <button @click="$emit('join', challenge.id)">→</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  challenge: Object
})

// 카테고리 색상 매핑
const categoryColorMap = {
  '소설': '#ffe0cc',
  '자기계발': '#e0d4ff',
  '여행': '#ccf0ff',
  '기본': '#f5f5f5'
}

// 배경색 선택
const backgroundColor = computed(() => {
  return categoryColorMap[props.challenge.book.category?.name] || categoryColorMap['기본']
})

// 기간 포맷팅
const formattedPeriod = computed(() => {
  const start = props.challenge.start_date?.slice(0, 10)
  const end = props.challenge.end_date?.slice(0, 10)
  return start && end ? `${start} ~ ${end}` : ''
})
</script>

<style scoped>
.challenge-item {
  padding: 1.25rem;
  border-radius: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  transition: transform 0.2s;
}
.challenge-item:hover {
  transform: translateY(-5px);
}

.cover-wrapper img {
  width: 100%;
  border-radius: 0.75rem;
  object-fit: cover;
  height: 140px;
  margin-bottom: 1rem;
}

.content h3 {
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 0.3rem;
}
.content p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.period {
  font-size: 0.8rem;
  color: #999;
  margin: 0.5rem 0;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer button {
  background: #fff;
  color: #555;
  border: 1px solid #ccc;
  transition: all 0.2s ease;
}
.footer button:hover {
  background: #2cd99c;
  color: white;
  border-color: transparent;
}
</style>
