<template>
  <div class="text-center">
    <!-- 책 표지 이미지 -->
    <div class="position-relative d-inline-block">
      <img :src="book.cover" class="book-cover mb-2" alt="책 표지" />
      <span
        v-if="showFavorite"
        class="heart-toggle"
        @click="togglePreferred"
      >
        {{ isPreferredComputed ? "♥" : "♡" }}
      </span>
    </div>

    <!-- 책 정보 -->
    <div class="fw-semibold text-truncate" :title="book.title">
      {{ book.title }}
    </div>
    <div class="text-muted small">
      {{ book.author }}<br />
      {{ book.publisher }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  book: Object,
  isPreferred: {
    type: Boolean,
    default: undefined
  }
})

const emits = defineEmits(['toggle-preferred'])

const isPreferredComputed = computed(() => props.isPreferred)
const showFavorite = computed(() => props.isPreferred !== undefined)

const togglePreferred = () => {
  emits('toggle-preferred', props.book.id)
}
</script>

<style scoped>
.book-cover {
  width: 150px;
  height: 220px;
  object-fit: cover;
  border-radius: 0.25rem;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}

/* 하트 위치 */
.heart-toggle {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 1.5rem;
  color: #c0392b;
  cursor: pointer;
  user-select: none;
}
</style>
