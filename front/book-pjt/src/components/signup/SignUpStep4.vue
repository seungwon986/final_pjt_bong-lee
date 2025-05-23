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

    <!-- <div class="mt-4 d-flex justify-content-between">
      <button class="btn btn-secondary" @click="$emit('prev')">이전</button>
      <button class="btn btn-success" @click="submitForm">회원가입 완료</button>
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'

const props = defineProps({
  form: Object
})
const store = useAccountStore()

const categoryNames = ref([])
const bookTitles = ref([])

onMounted(() => {
  // 카테고리 이름 불러오기
  axios.get('http://127.0.0.1:8000/api/v1/books/categories/')
    .then(res => {
      const map = {}
      res.data.forEach(cat => map[cat.id] = cat.name)
      categoryNames.value = props.form.preferred_categories.map(id => map[id]).filter(Boolean)
    })

  // 도서 제목 불러오기
  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then(res => {
      const map = {}
      res.data.forEach(book => map[book.id] = book.title)
      bookTitles.value = props.form.preferred_books.map(id => map[id]).filter(Boolean)
    })
})

const submitForm = () => {
  const {
    username, password1, password2, nickname, first_name, last_name,
    gender, birth, preferred_categories, preferred_books, profile_image
  } = props.form

  // 유효성 검증
  if (!username || !password1 || !password2 || !nickname || !first_name || !last_name || !gender || !birth || !preferred_categories.length || !preferred_books.length) {
    alert('모든 항목을 올바르게 입력했는지 확인해주세요.')
    return
  }

  // FormData로 전환
  const data = new FormData()
  data.append('username', username)
  data.append('password1', password1)
  data.append('password2', password2)
  data.append('nickname', nickname)
  data.append('first_name', first_name)
  data.append('last_name', last_name)
  data.append('gender', gender)
  data.append('birth', birth)

  preferred_categories.forEach(cat => data.append('preferred_categories', cat))
  preferred_books.forEach(book => data.append('preferred_books', book))

  if (profile_image) {
    data.append('profile_image', profile_image)
  }

  store.signUp(data)
}
</script>

<style scoped>
</style>
