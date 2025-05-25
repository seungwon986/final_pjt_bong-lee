<template>
  <div class="book-slider">
    <div class="slider-wrapper">
      <div class="book-card" v-for="book in books" :key="book.id">
        <img :src="book.cover" :alt="book.title" class="book-cover" />
        <div class="book-info">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">{{ book.author }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  books: {
    type: Array,
    required: true,
  },
})
</script>

<style scoped>
.book-slider {
  overflow-x: auto;
  white-space: nowrap;
  padding-bottom: 1rem;
}

.slider-wrapper {
  display: flex;
  gap: 1.5rem;
}

.book-card {
  display: inline-block;
  width: 160px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.book-card:hover {
  transform: translateY(-4px);
}

.book-cover {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.book-info {
  padding: 0.8rem;
  text-align: center;
}

.book-title {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.3rem;
}

.book-author {
  font-size: 0.85rem;
  color: #888;
}
</style>
