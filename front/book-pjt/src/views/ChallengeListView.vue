
<template>
  <div class="container py-4">
    <h2 class="mb-4">📘 챌린지 목록</h2>

    <!-- 카테고리 필터 -->
    <div class="category-tabs mb-4">
      <button
        v-for="cat in categories"
        :key="cat"
        :class="{ active: cat === activeCategory }"
        @click="activeCategory = cat"
      >
        {{ cat }}
      </button>
    </div>

    <!-- 챌린지 목록 -->
    <div v-if="filteredChallenges.length" class="challenge-list">
      <ChallengeItem
        v-for="challenge in filteredChallenges"
        :key="challenge.id"
        :challenge="challenge"
      />
    </div>
    <div v-else>
      <p>해당 카테고리에 챌린지가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import ChallengeItem from '@/components/main/ChallengeItem.vue'

const store = useAccountStore()
const API_URL = 'http://127.0.0.1:8000/api/v1'

const challenges = ref([])
const activeCategory = ref('전체')

// 챌린지 불러오기
const fetchChallenges = async () => {
  try {
    const res = await axios.get(`${API_URL}/challenges/`)
    challenges.value = res.data
  } catch (err) {
    console.error('챌린지 로드 실패:', err)
  }
}

onMounted(() => {
  fetchChallenges()
})

// 카테고리 목록 추출
const categories = computed(() => {
  const set = new Set(challenges.value.map(c => c.category).filter(Boolean))
  return ['전체', ...set]
})

// 선택된 카테고리 기준 필터링
const filteredChallenges = computed(() => {
  if (activeCategory.value === '전체') return challenges.value
  return challenges.value.filter(c => c.category === activeCategory.value)
})
</script>

<style scoped>
.category-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.category-tabs button {
  padding: 0.4rem 0.9rem;
  border: none;
  border-radius: 999px;
  background-color: #f2f2f2;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}
.category-tabs button.active {
  background-color: #2cd99c;
  color: white;
}
</style>
