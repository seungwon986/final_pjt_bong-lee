<template>
  <div>
    <p>관심 있는 카테고리 기반으로 선호 도서를 골라주세요</p>

    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="book in books" :key="book.id">
        <div
          class="card h-100"
          :class="{ 'selected': selected.includes(book.id) }"
          @click="toggle(book.id)"
        >
          <img :src="book.cover" class="card-img-top" alt="book cover" />
          <div class="card-body">
            <h5 class="card-title">{{ book.title }}</h5>
            <p class="card-text">{{ book.author }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4 d-flex justify-content-between">
      <button type="button" class="btn btn-secondary" @click="emit('prev')">이전</button>
      <button type="button" class="btn btn-primary" @click="handleNext">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  form: Object
})
const emit = defineEmits(['next', 'prev'])

const books = ref([])
const selected = ref([])

const toggle = (bookId) => {
  const idx = selected.value.indexOf(bookId)
  if (idx === -1) {
    selected.value.push(bookId)
  } else {
    selected.value.splice(idx, 1)
  }
}

const handleNext = () => {
  if (selected.value.length === 0) {
    alert('선호하는 도서를 한 권 이상 선택해주세요.')
    return
  }
  props.form.preferred_books = [...selected.value]
  emit('next')
}

const fetchBooksByCategories = async () => {
  const categoryIds = props.form.preferred_categories
  if (!Array.isArray(categoryIds) || categoryIds.length === 0) return

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/books/')
    books.value = res.data.filter(book => {
      const bookCategoryId = typeof book.category === 'object' ? book.category?.id : book.category
      return categoryIds.map(Number).includes(Number(bookCategoryId))
    })

    // 기존 선택 복원
    if (props.form.preferred_books?.length > 0) {
      selected.value = [...props.form.preferred_books]
    }

  } catch (err) {
    console.error('도서 불러오기 실패:', err)
  }
}

onMounted(fetchBooksByCategories)
watch(() => props.form.preferred_categories, fetchBooksByCategories, { immediate: true })
</script>

<style scoped>
.card {
  cursor: pointer;
  transition: transform 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-4px);
}

.card-img-top {
  height: 100%;
  width: 100%;
  object-fit: cover;
}

.card-body {
  padding: 0.8rem;
}

.card-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  min-height: 2.8em;
}

.card-text {
  font-size: 0.7rem;
  color: #555;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card.selected {
  border: 2px solid #fc47b0;
}
</style>
