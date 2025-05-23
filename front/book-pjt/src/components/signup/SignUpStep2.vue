<template>
  <div>
    <p>관심 있는 카테고리를 선택하세요</p>
    <div class="row row-cols-2 row-cols-md-4 g-3">
      <div
        class="col"
        v-for="category in categories"
        :key="category.id"
        @click="toggleCategory(category.id)"
      >
        <div
          class="card text-center h-100 p-2"
          :class="{ 'border-primary': selected.includes(category.id) }"
        >
          {{ category.name }}
        </div>
      </div>
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

      // ✅ 이미 선택된 카테고리 있으면 복원
      if (props.form.preferred_categories?.length > 0) {
        selected.value = [...props.form.preferred_categories]
      }
    })
    .catch(err => {
      console.error('카테고리 불러오기 실패:', err)
    })
})
</script>

<style scoped>
.card {
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 12px 18px;
  cursor: pointer;
  transition: all 0.2s ease;
}
p {
  text-align: center;
  padding-bottom: 50px;
}

.card:hover {
  background: #f07ac834;
}
.card.border-primary {
  border: 2px solid #f36faa;  
  background-color: #eec1d6;  
  color: #ee5f9f;
  font-weight: bold;
  transition: background-color 0.2s, border-color 0.2s;
}

</style>
