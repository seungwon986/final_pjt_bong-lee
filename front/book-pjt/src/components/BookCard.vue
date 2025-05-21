<template>
  <div class="card h-100 shadow-sm border-0">
    <img
      :src="book.cover"
      class="card-img-top object-fit"
      alt="책 표지"
    />
    <div class="card-body d-flex flex-column">
      <h5 class="card-title text-truncate" :title="book.title">{{ book.title }}</h5>
      <p class="card-text text-muted mb-1">👤 {{ book.author }}</p>
      <p class="card-text small text-muted mb-2">🏢 {{ book.publisher }} | 📅 {{ formattedDate }}</p>
      <div class="mt-auto">
        <span class="badge bg-warning text-dark">⭐ {{ book.customer_review_rank }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  book: Object
})

const formattedDate = computed(() => {
  if (!props.book.pub_date) return ''
  return new Date(props.book.pub_date).toLocaleDateString('ko-KR')
})
</script>

<style scoped>
.card-img-top {
  height: 240px;
  object-fit: cover;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .card-img-top {
    height: 200px;
  }
}
</style>
