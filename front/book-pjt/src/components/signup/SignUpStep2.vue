<template>
  <div>
    <h3>관심 있는 카테고리를 선택하세요</h3>
    <div class="row row-cols-2 row-cols-md-4 g-3">
      <div
        class="col"
        v-for="category in categories"
        :key="category.id"
        @click="toggleCategory(category.id)"
      >
        <div
          class="card h-100 text-center p-2"
          :class="{ 'border-primary': selected.includes(category.id) }"
        >
          {{ category.name }}
        </div>
      </div>
    </div>

    <div class="mt-4 d-flex justify-content-between">
      <button class="btn btn-secondary" @click="$emit('prev')">이전</button>
      <button class="btn btn-primary" @click="handleNext">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  form: Object
})

const emit = defineEmits(['next', 'prev'])

const categories = ref([])
const selected = ref([])

const toggleCategory = (id) => {
  const idx = selected.value.indexOf(id)
  if (idx === -1) {
    selected.value.push(id)
  } else {
    selected.value.splice(idx, 1)
  }
}

const handleNext = () => {
  if (selected.value.length === 0) {
    alert('관심 있는 카테고리를 한 개 이상 선택해주세요.')
    return
  }

  props.form.preferred_categories = selected.value
  emit('next')
}

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/categories/')
    .then(res => {
      categories.value = res.data
    })
    .catch(err => {
      console.error('카테고리 불러오기 실패:', err)
    })
})
</script>

<style scoped>
.card {
  cursor: pointer;
}
</style>
