<template>
  <div>
    <p>선호 카테고리를 선택해주세요</p>
    <div v-for="category in categories" :key="category.id" class="form-check">
      <input
        type="checkbox"
        :id="'cat-' + category.id"
        class="form-check-input"
        :value="category.id"
        v-model="model"
      />
      <label :for="'cat-' + category.id" class="form-check-label">
        {{ category.name }}
      </label>
    </div>
    <div class="mt-3">
      <button class="btn btn-secondary" @click="$emit('prev')">이전</button>
      <button class="btn btn-primary" @click="$emit('next')">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:selectedCategories', 'next', 'prev'])

const categories = ref([])


const model = ref(Array.isArray(props.modelValue) ? [...props.modelValue] : [])

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/categories/')
    .then(res => categories.value = res.data)
    .catch(err => console.error('카테고리 불러오기 실패', err))
})

watch(model, () => emit('update:selectedCategories', model.value))
</script>
