<template>
  <div>
    <h3>입력 정보를 확인하고 회원가입을 완료하세요</h3>
    <ul class="list-group my-4">
      <li class="list-group-item"><strong>아이디:</strong> {{ form.username }}</li>
      <li class="list-group-item"><strong>닉네임:</strong> {{ form.nickname }}</li>
      <li class="list-group-item"><strong>이름:</strong> {{ form.first_name }} {{ form.last_name }}</li>
      <li class="list-group-item"><strong>성별:</strong> {{ form.gender === 'M' ? '남성' : '여성' }}</li>
      <li class="list-group-item"><strong>생년월일:</strong> {{ form.birth }}</li>
      <li class="list-group-item"><strong>관심 카테고리:</strong> {{ categoryNames.join(', ') }}</li>
      <li class="list-group-item"><strong>선호 도서:</strong> {{ bookTitles.join(', ') }}</li>
    </ul>

    <div class="mt-4 d-flex justify-content-between">
      <button class="btn btn-secondary" @click="$emit('prev')">이전</button>
      <button class="btn btn-success" @click="$emit('submit')">회원가입 완료</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({ form: Object })
const emit = defineEmits(['submit', 'prev'])

const categoryNames = ref([])
const bookTitles = ref([])

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/categories/')
    .then(res => {
      const map = {}
      res.data.forEach(cat => map[cat.id] = cat.name)
      categoryNames.value = props.form.preferred_categories.map(id => map[id]).filter(Boolean)
    })

  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then(res => {
      const map = {}
      res.data.forEach(book => map[book.id] = book.title)
      bookTitles.value = props.form.preferred_books.map(id => map[id]).filter(Boolean)
    })
})
</script>

<style scoped>
.list-group {
  font-size: 0.95rem;
  padding: 0;
}

.list-group-item {
  padding: 0.75rem 1rem;
  border: 1px solid #eee;
  margin-bottom: 6px;
}

.btn {
  padding: 8px 16px;
  font-size: 0.9rem;
}
</style>
