<template>
  <div>
    <p>선택한 카테고리 기반으로 선호 도서를 골라주세요</p>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col" v-for="book in books" :key="book.id">
        <div
          class="card h-100"
          :class="{ 'border-primary': internalModel.includes(book.id) }"
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
    <div class="mt-3">
      <button class="btn btn-secondary" @click="$emit('prev')">이전</button>
      <button class="btn btn-primary" @click="$emit('next')">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'

// ✅ props: selectedBooks (v-model) & selectedCategories (for filtering)
const props = defineProps({
  selectedBooks: {
    type: Array,
    default: () => []
  },
  selectedCategories: {
    type: Array,
    default: () => []
  }
})

// ✅ emits: selectedBooks 업데이트, 단계 이동
const emit = defineEmits(['update:selectedBooks', 'prev', 'next'])

const books = ref([])
const internalModel = ref([]) // 내부 선택 상태

// ✅ props로 받은 초기 선택 상태 반영
onMounted(() => {
  internalModel.value = [...props.selectedBooks]

  if (props.selectedCategories.length === 0) return

  const query = props.selectedCategories.map((c) => `category=${c}`).join('&')
  axios.get(`http://127.0.0.1:8000/api/v1/books/?${query}`)
    .then((res) => {
      books.value = res.data
    })
    .catch((err) => {
      console.error('도서 불러오기 실패', err)
    })
})

// ✅ internalModel이 바뀌면 selectedBooks로 emit
watch(internalModel, () => {
  emit('update:selectedBooks', internalModel.value)
})

const toggle = (id) => {
  if (internalModel.value.includes(id)) {
    internalModel.value = internalModel.value.filter((i) => i !== id)
  } else {
    internalModel.value.push(id)
  }
}
</script>
