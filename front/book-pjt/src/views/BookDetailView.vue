<template>
  <div class="book-detail-container">
    <!-- 왼쪽: 책 표지 -->
    <div class="book-cover-wrapper">
      <img :src="book.cover" alt="책 표지" class="book-cover" />
    </div>

    <!-- 오른쪽: 책 정보 -->
    <div class="book-info">
      <h1 class="book-title">{{ book.title }}</h1>
      <p class="book-author">저자: {{ book.author }}</p>
      <p class="book-publisher">출판사: {{ book.publisher }}</p>
      <p class="book-date">출판일: {{ formattedDate(book.pub_date) }}</p>
      <p class="book-description">{{ book.description }}</p>

      <RouterLink
        :to="{ name: 'ChallengeCreate', query: {
          book_id: book.id,
          title: book.title,
          author: book.author
        }}"
        class="challenge-btn"
      >
        📚 이 책으로 챌린지 하기
      </RouterLink>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const book = ref({})

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:8000/api/v1/books/${route.params.id}/`)
  book.value = res.data
})

function formattedDate(dateString) {
  return new Date(dateString).toLocaleDateString('ko-KR')
}
</script>


<style scoped>
.book-detail-container {
  display: flex;
  flex-direction: row;
  gap: 3rem;
  max-width: 1080px;
  margin: 4rem auto;
  padding: 0 1rem;
  align-items: flex-start;
  font-family: 'Pretendard', sans-serif;
}

/* 표지 이미지 */
.book-cover-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
}
.book-cover {
  width: 100%;
  max-width: 320px;
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(0,0,0,0.1);
  object-fit: cover;
}

/* 텍스트 정보 */
.book-info {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.book-title {
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.4;
}
.book-author,
.book-publisher,
.book-date {
  font-size: 1rem;
  color: #444;
}
.book-description {
  font-size: 1rem;
  color: #333;
  line-height: 1.7;
  white-space: pre-line;
}

/* 챌린지 버튼 */
.challenge-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.85rem 2rem;
  background-color: #2cd99c;
  color: #fff;
  font-weight: 600;
  border-radius: 8px;
  transition: background 0.3s ease;
  text-align: center;
  width: fit-content;
}
.challenge-btn:hover {
  background-color: #1dbd85;
}
</style>

