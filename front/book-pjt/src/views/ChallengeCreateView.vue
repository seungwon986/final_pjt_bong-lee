<template>
  <div class="challenge-create">
    <h2>📘 챌린지 만들기</h2>

    <form @submit.prevent="onSubmit">

      <!-- 제목 -->
      <label>챌린지 제목
        <input v-model="title" required />
      </label>

      <!-- 카테고리 선택 -->
      <label>카테고리
        <select v-model="category" required>
          <option disabled value="">선택하세요</option>
          <option v-for="cat in categories" :key="cat">{{ cat }}</option>
        </select>
      </label>

     <!-- 검색창 -->
<input
  type="text"
  v-model="bookQuery"
  placeholder="도서명을 검색하세요"
  class="search-input"
/>

<!-- 검색 결과 리스트 -->
<ul v-if="filteredBookResults.length" class="search-dropdown">
  <li
    v-for="book in filteredBookResults"
    :key="book.id"
    @click="selectBook(book)"
    class="search-item"
  >
    <img :src="book.cover" alt="cover" class="book-cover" />
    <div class="book-info">
      <strong>{{ book.title }}</strong>
      <p>{{ book.author }} · {{ book.publisher }}</p>
    </div>
  </li>
</ul>


      <!-- 책 표지 자동 표시 -->
      <div v-if="selectedBookCover" class="cover-preview">
        <img :src="selectedBookCover" alt="책 표지" />
      </div>

      <!-- 인원 설정 -->
      <label>최대 참여 인원
        <input type="number" v-model.number="maxParticipants" min="2" required />
      </label>

      <!-- 모집 소개글 -->
      <label>소개글
        <textarea v-model="description" required></textarea>
      </label>

      <!-- 날짜 설정 -->
      <label>모집 마감일
        <input type="date" v-model="deadline" />
      </label>

      <label>시작일
        <input type="date" v-model="startDate" />
      </label>

      <label>진행 기간 (일)
        <input type="number" v-model.number="duration" min="1" />
      </label>

      <button type="submit">챌린지 등록</button>
    </form>
  </div>
</template>


<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { useChallengeStore } from '@/stores/challenge.js'
import { useRouter } from 'vue-router'

const store = useChallengeStore()
const router = useRouter()

// 입력 폼 상태
const title = ref('')
const category = ref('')
const description = ref('')
const coverUrl = ref('')

// 📚 책 목록과 카테고리 추출
const books = ref([])

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/v1/books/')
    .then(res => {
      books.value = res.data
    })
})

const categories = computed(() => {
  const nameSet = new Set()
  books.value.forEach(book => {
    if (book.category?.name) {
      nameSet.add(book.category.name)
    }
  })
  return Array.from(nameSet)
})


const bookQuery = ref('')
const selectedBook = ref(null)

const filteredBookResults = computed(() => {
  return books.value.filter(book =>
    book.title.toLowerCase().includes(bookQuery.value.toLowerCase())
  )
})

function selectBook(book) {
  selectedBook.value = book
  bookQuery.value = book.title  // 선택되면 input에 제목 자동 입력
}

// 기간 자동 계산
const startDate = ref('')
const deadline = ref('')

const duration = computed(() => {
  if (!startDate.value || !deadline.value) return ''
  const start = new Date(startDate.value)
  const end = new Date(deadline.value)
  const diff = (end - start) / (1000 * 60 * 60 * 24)
  return diff >= 0 ? diff : ''
})


// 제출 핸들러
function onSubmit() {
  store.createChallenge({
    title: title.value,
    category: category.value,
    description: description.value,
    coverUrl: coverUrl.value || ''
  })

  router.push('/challenge/list')
}

watch(category, () => {
  bookQuery.value = ''
  selectedBook.value = null
})
</script>


<style scoped>
.create-page {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #fffefc;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input, select, textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem;
  background-color: #1677ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #135ce0;
}

.search-input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-dropdown {
  list-style: none;
  margin: 0.5rem 0 0;
  padding: 0;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
  background: white;
  position: absolute;
  z-index: 1000;
  width: 100%;
}

.search-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.search-item:hover {
  background: #f0f8ff;
}

.book-cover {
  width: 40px;
  height: 60px;
  object-fit: cover;
  margin-right: 1rem;
  border-radius: 4px;
}

.book-info {
  display: flex;
  flex-direction: column;
}
</style>


