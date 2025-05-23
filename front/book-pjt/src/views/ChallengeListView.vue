<template>
  <div class="challenge-page">
    <!-- 카테고리 탭 -->
    <CategoryTabs
      :categories="store.categories"
      :active="store.activeCategory"
      @select="store.selectCategory"
    />

    <!-- 로딩 / 에러 / 챌린지 목록 -->
    <div v-if="store.loading" class="message">로딩 중...</div>
    <div v-else-if="store.error" class="message error">{{ store.error }}</div>
    <div v-else class="challenge-list-container">
      <ChallengeList :challenges="store.filteredChallenges" />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useChallengeStore } from '@/stores/challenge'
import CategoryTabs from '@/components/challenge/CategoryTabs.vue'
import ChallengeList from '@/components/challenge/ChallengeList.vue'

const store = useChallengeStore()

onMounted(async () => {
  await store.loadCategories()
  await store.loadChallenges()
})
</script>

<style scoped>
.challenge-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.challenge-list-container {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.message {
  text-align: center;
  padding: 1rem;
  color: #666;
}
.message.error {
  color: #d9534f;
}
</style>
