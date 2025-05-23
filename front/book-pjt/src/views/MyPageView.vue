<template>
  <div class="container py-4">
    <h2 class="mb-4">📖 마이페이지</h2>

    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="border p-2 text-center">
          <img
            :src="imageUrl(user.profile_image)"
            alt="프로필"
            class="img-fluid rounded"
          />
          <p class="mt-2 fw-semibold">{{ user.nickname }}</p>
        </div>
      </div>

      <div class="col-md-9 mb-4">
        <div class="border p-3">
          <h5>회원 정보</h5>
          <p>이름: {{ user.last_name }}{{ user.first_name }}</p>
          <p>이메일: {{ user.email }}</p>
          <p>팔로잉: {{ user.following_count }}명 | 팔로워: {{ user.follower_count }}명</p>
        </div>

        <div class="border p-3 mt-3">
          <h5>내가 쓴 글</h5>
          <p class="text-muted">게시글 카드 or 리스트 삽입 예정</p>
        </div>
      </div>
    </div>

    <div class="border p-3 mb-4">
      <h5>📚 내 취향 책 (내 책장)</h5>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <BookCard
          v-for="book in books"
          :key="book.id"
          :book="book"
          :is-preferred="true"
          @toggle-preferred="togglePreferred"
        />
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 mb-4">
        <div class="border p-3">
          <h5>🔥 참여한 챌린지</h5>
          <p class="text-muted">챌린지 요약 정보 or 카드</p>
        </div>
      </div>

      <div class="col-md-6 mb-4">
        <div class="border p-3">
          <h5>📚 참여 중인 북클럽</h5>
          <p class="text-muted">북클럽 요약 정보</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'
import BookCard from '@/components/BookCard.vue'

const store = useAccountStore()
const user = computed(() => store.user)
const books = ref([])

const imageUrl = (path) => {
  if (!path) return '/default-profile.png'
  if (path.startsWith('http')) return path
  return `http://127.0.0.1:8000${path}`
}

const fetchPreferredBooks = async (bookIds) => {
  if (!bookIds || bookIds.length === 0) {
    books.value = []
    return
  }
  try {
    const promises = bookIds.map(id =>
      axios.get(`http://127.0.0.1:8000/api/v1/books/${id}/`)
    )
    const responses = await Promise.all(promises)
    books.value = responses.map(res => res.data)
  } catch (err) {
    console.error('도서 정보 불러오기 실패:', err)
  }
}

const togglePreferred = async (bookId) => {
  try {
    const current = store.user?.preferred_books || []
    const updated = current.includes(bookId)
      ? current.filter(id => id !== bookId)
      : [...current, bookId]

    await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      preferred_books: updated
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })

    await store.fetchUserProfile()
    fetchPreferredBooks(store.user.preferred_books)

  } catch (err) {
    console.error('선호 도서 토글 실패:', err)
  }
}

onMounted(async () => {
  await store.fetchUserProfile()
  fetchPreferredBooks(store.user.preferred_books)
})
</script>

<style scoped>
img {
  max-height: 150px;
  object-fit: cover;
}
</style>
