<template>
  <div class="challenge-create-wrapper">
    <h2>챌린지 생성</h2>
    <form @submit.prevent="submitChallenge">
      <!-- 최대 참여 인원 -->
      <div class="form-group">
        <label for="maxParticipants">최대 참여 인원</label>
        <input
          id="maxParticipants"
          type="number"
          v-model.number="form.maxParticipants"
          min="1"
          required
        />
      </div>

      <!-- 도서 카테고리 선택 -->
      <div class="form-group">
        <label for="category">도서 카테고리</label>
        <select id="category" v-model="form.category" required>
          <option value="" disabled>카테고리 선택</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>

      <!-- 도서명 검색 -->
      <div class="form-group">
        <label for="bookSearch">도서명 검색</label>
        <input
          id="bookSearch"
          type="text"
          v-model="searchQuery"
          @input="fetchSuggestions"
          placeholder="책 제목을 입력하세요"
          autocomplete="off"
        />
        <ul v-if="suggestions.length" class="suggestions-list">
          <li v-for="book in suggestions" :key="book.id" @click="selectBook(book)">
            {{ book.title }} - {{ book.author }}
          </li>
        </ul>
      </div>

      <!-- 선택된 도서 -->
      <div class="form-group" v-if="form.book">
        <label>선택 도서</label>
        <div class="selected-book">
          <img :src="form.book.cover" :alt="form.book.title" />
          <div class="info">
            <p class="title">{{ form.book.title }}</p>
            <p class="author">{{ form.book.author }}</p>
          </div>
        </div>
      </div>

      <!-- 소개글 -->
      <div class="form-group">
        <label for="description">소개글</label>
        <textarea id="description" v-model="form.description" rows="4" required></textarea>
      </div>

      <!-- 시작일 & 마감일 -->
      <div class="form-group date-group">
        <div>
          <label for="startDate">시작일</label>
          <input id="startDate" type="date" v-model="form.startDate" required />
        </div>
        <div>
          <label for="endDate">마감일</label>
          <input id="endDate" type="date" v-model="form.endDate" required />
        </div>
      </div>

      <!-- 진행 기간 -->
      <div class="form-group">
        <label>진행 기간</label>
        <input type="text" :value="duration" readonly />
      </div>

      <!-- 제출 버튼 -->
      <button type="submit" class="btn-submit">챌린지 생성</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import axios from 'axios'

const categories = ref(["인문", "에세이", "과학", "소설", "기술"])
const searchQuery = ref('')
const suggestions = ref([])

const form = reactive({
  maxParticipants: 5,
  category: '',
  book: null,
  description: '',
  startDate: '',
  endDate: ''
})

// 도서 자동완성
const fetchSuggestions = async () => {
  if (!searchQuery.value) {
    suggestions.value = []
    return
  }
  try {
    const { data } = await axios.get(`/api/books?search=${encodeURIComponent(searchQuery.value)}`)
    suggestions.value = data
  } catch (e) {
    console.error(e)
  }
}

// 도서 선택
function selectBook(book) {
  form.book = book
  suggestions.value = []
  searchQuery.value = book.title
}

// 진행 기간 계산
const duration = computed(() => {
  if (!form.startDate || !form.endDate) return ''
  const start = new Date(form.startDate)
  const end = new Date(form.endDate)
  const diff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1
  return `${diff}일`
})

// 날짜 검증
watch(() => form.startDate, () => {
  if (form.endDate && form.endDate < form.startDate) {
    form.endDate = ''
  }
})

// 제출 처리
const submitChallenge = async () => {
  const payload = {
    maxParticipants: form.maxParticipants,
    category: form.category,
    bookId: form.book?.id,
    description: form.description,
    startDate: form.startDate,
    endDate: form.endDate
  }
  try {
    await axios.post('/api/challenges', payload)
    alert('챌린지가 생성되었습니다!')
    // TODO: 페이지 이동 또는 초기화 등 추가 작업
  } catch (e) {
    console.error(e)
    alert('생성 중 오류가 발생했습니다.')
  }
}



import { useRoute } from 'vue-router'
const route = useRoute()

const bookId = route.query.book_id
const prefillTitle = route.query.title
const prefillAuthor = route.query.author


</script>

<style scoped>
.challenge-create-wrapper {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.challenge-create-wrapper h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: #2c3e50;
}
.form-group {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}
.form-group label {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #34495e;
}
.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #dcdfe6;
  border-radius: 0.5rem;
}
.date-group {
  display: flex;
  gap: 1rem;
}
.suggestions-list {
  margin: 0.25rem 0 0;
  padding: 0;
  list-style: none;
  border: 1px solid #dcdfe6;
  border-radius: 0.5rem;
  max-height: 150px;
  overflow-y: auto;
  background: #fff;
}
.suggestions-list li {
  padding: 0.5rem;
  cursor: pointer;
}
.suggestions-list li:hover {
  background: #f0f2f5;
}
.selected-book {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
.selected-book img {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: 0.25rem;
}
.selected-book .info p {
  margin: 0;
  font-size: 0.875rem;
  color: #2c3e50;
}
.btn-submit {
  width: 100%;
  padding: 0.75rem;
  background: #2c3e50;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
}
.btn-submit:hover {
  background: #1a252f;
}
</style>
