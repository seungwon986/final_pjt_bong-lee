<template>
  <div>
    <p>선택한 카테고리 기반으로 선호 도서를 골라주세요</p>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="book in books" :key="book.id">
        <div
          class="card h-100"
          :class="{ 'border-primary': selected.includes(book.id) }"
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

  props.form.preferred_books = selected.value
  emit('next')
}

const fetchBooksByCategories = () => {
  const categoryIds = props.form.preferred_categories
  if (!categoryIds || categoryIds.length === 0) return

  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then(res => {
     books.value = res.data.filter(book => {
  const bookCategoryId = typeof book.category === 'object' ? book.category.id : book.category
  return categoryIds.map(Number).includes(Number(bookCategoryId))
})
    })
    .catch(err => console.error('도서 불러오기 실패:', err))
}

onMounted(fetchBooksByCategories)
watch(() => props.form.preferred_categories, fetchBooksByCategories, { immediate: true })
</script>

<style scoped>
.card {
  cursor: pointer;
}
p {
  text-align: center;
}
</style>
