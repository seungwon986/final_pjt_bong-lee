<template>
  <div class="container py-4 d-flex">
    <!-- 사이드바: 카테고리 리스트 -->
    <aside class="sidebar pe-4">
      <h3 class="mb-3">카테고리</h3>
      <ul class="sidebar-cats">
        <li
          v-for="cat in categories"
          :key="cat"
          :class="{ active: cat === activeCategory }"
          @click="activeCategory = cat"
        >
          {{ cat }}
        </li>
      </ul>
    </aside>

    <!-- 메인: 챌린지 목록 -->
    <main class="flex-fill">
      <h2 class="mb-4">📘 챌린지 목록</h2>

      <div v-if="filteredChallenges.length" class="challenge-list grid">
        <ChallengeItem
          v-for="challenge in filteredChallenges"
          :key="challenge.id"
          :challenge="challenge"
        />
      </div>
      <div v-else>
        <p>해당 카테고리에 챌린지가 없습니다.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import ChallengeItem from '@/components/main/ChallengeItem.vue'

const store = useAccountStore()
const route = useRoute()
const API_URL = 'http://127.0.0.1:8000/api/v1'

const challenges = ref([])
const activeCategory = ref('전체')

// 챌린지 호출 (인증 필요 시 헤더 추가)
const fetchChallenges = async () => {
  try {
    const res = await axios.get(
      `${API_URL}/challenges/`,
      { headers: { Authorization: `Token ${store.token}` } }
    )
    console.log('🔍 API 응답:', res.data)
    challenges.value = res.data
  } catch (err) {
    console.error('챌린지 로드 실패:', err)
  }
}

onMounted(fetchChallenges)
watch(challenges, v => console.log('🔍 challenges 변경:', v), { deep: true })

// 쿼리 파라미터로도 카테고리 제어
watch(
  () => route.query.category,
  newCat => {
    activeCategory.value = newCat || '전체'
  },
  { immediate: true }
)

// 카테고리 리스트 생성
const categories = computed(() => {
  const set = new Set(
    challenges.value
      .map(c => c.book?.category?.name)
      .filter(Boolean)
  )
  return ['전체', ...set]
})

// 선택된 카테고리로 필터링
const filteredChallenges = computed(() => {
  if (activeCategory.value === '전체') {
    return challenges.value
  }
  return challenges.value.filter(
    c => c.book?.category?.name === activeCategory.value
  )
})
</script>

<style scoped>
/* 컨테이너는 flex 유지 */
.container.d-flex {
  display: flex;
  flex-wrap: wrap;
}

/* 사이드바 */
.sidebar {
  width: 220px;
  border-right: 1px solid #e0e0e0;
  margin-left: 0; /* 기본값 (모바일 등에서 안 밀림) */
}

/* 데스크탑 이상에서만 왼쪽으로 당김 */
@media (min-width: 992px) {
  .sidebar {
    margin-left: -1.5rem;
  }
}

.sidebar h3 {
  font-size: 1.125rem;
  margin-bottom: 0.75rem;
}

.sidebar-cats {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-cats li {
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.sidebar-cats li:hover {
  background-color: #f5f5f5;
}

.sidebar-cats li.active {
  background-color: #2cd99c;
  color: white;
}

/* 챌린지 그리드 */
.challenge-list.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}

/* 버튼탭은 숨김 */
.category-tabs {
  display: none;
}
</style>
