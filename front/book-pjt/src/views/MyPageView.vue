<template>
  <div v-if="user" class="container py-4">
    <h2 class="mb-4">📖 마이페이지</h2>

    <!-- 프로필 -->
    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="border p-2 text-center">
          <img :src="imageUrl(user.profile_image)" alt="프로필" class="img-fluid rounded" />
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

    <!-- 선호 도서 -->
    <div class="border p-3 mb-4">
      <h5>📚 내 취향 책 (내 책장)</h5>
      <div class="book-grid">
        <div class="book-card" v-for="book in preferredBooks" :key="book.id">
          <img :src="book.cover || '/default-book-cover.png'" :alt="book.title" class="book-cover" />
          <div class="book-info">
            <div class="title-wrap">
              <h3 class="book-title clamp">{{ book.title }}</h3>
              <label class="heart-label">
                <input type="checkbox" :checked="isLiked(book.id)" @change="togglePreferred(book.id)" class="heart-checkbox" />
                <svg class="icon" viewBox="0 0 1024 1024">
                  <path
                    class="heart-path"
                    d="M742.4 101.12A249.6 249.6 0 0 0 512 256a249.6
                       249.6 0 0 0-230.72-154.88C143.68 101.12 32 238.4
                       32 376.32c0 301.44 416 546.56 480 546.56s480-245.12
                       480-546.56c0-137.92-111.68-275.2-249.6-275.2z"
                  />
                </svg>
                <span class="burst"></span>
              </label>
            </div>
            <p class="book-author">👤 {{ book.author }}</p>
            <p class="book-publisher">🏢 {{ book.publisher }}</p>
            <p class="book-date">📅 {{ formattedDate(book.pub_date) }}</p>
            <p class="book-description">{{ book.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'

const store = useAccountStore()
const user = computed(() => store.user)
const preferredBooks = ref([])

const imageUrl = (path) => {
  if (!path) return '/default-profile.png'
  return path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`
}

const formattedDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const isLiked = (bookId) => {
  return store.user?.preferred_books.includes(bookId)
}

const fetchPreferredBooks = async () => {
  const bookIds = store.user?.preferred_books || []
  if (!bookIds.length) {
    preferredBooks.value = []
    return
  }
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/v1/books/preferred/', {
      preferred_books: bookIds,
    })
    preferredBooks.value = res.data
  } catch (err) {
    console.error('선호 도서 정보 불러오기 실패:', err)
  }
}

const togglePreferred = async (bookId) => {
  try {
    const current = store.user?.preferred_books || []
    const updated = current.includes(bookId)
      ? current.filter((id) => id !== bookId)
      : [...current, bookId]

    await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      preferred_books: updated,
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })

    await store.fetchUserProfile()
    await fetchPreferredBooks()
  } catch (err) {
    console.error('선호 도서 토글 실패:', err)
  }
}

onMounted(async () => {
  await store.fetchUserProfile()
  await fetchPreferredBooks()
})
</script>

<style scoped>
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.book-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: 0.3s ease all;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.book-cover {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.book-info {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.book-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0;
}

.title-wrap {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.book-author,
.book-publisher,
.book-date,
.book-description {
  font-size: 0.9rem;
  color: #555;
}

.clamp {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

/* ❤️ 하트 토글 스타일 */
.heart-label {
  position: relative;
  cursor: pointer;
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-left: 8px;
}

.heart-checkbox {
  display: none;
}

.icon {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: #ccc;
  stroke-width: 48;
  transition: stroke 0.3s ease;
  z-index: 2;
  position: relative;
}

.heart-checkbox:checked + .icon {
  fill: pink;
  stroke: pink;
}

/* ✅ ::v-deep으로 scoped 안에서 형제 burst 선택자 활성화 */
::v-deep(.heart-checkbox:checked ~ .burst) {
  opacity: 1;
  transform: scale(1.2);
  animation: pop 0.3s ease forwards;
}

.burst {
  position: absolute;
  top: 0;
  left: 0;
  width: 24px;
  height: 24px;
  background: radial-gradient(circle, rgba(255, 102, 102, 0.6) 20%, transparent 70%);
  border-radius: 50%;
  opacity: 0;
  transform: scale(0.6);
  transition: all 0.3s ease;
  pointer-events: none;
  z-index: 1;
}

@keyframes pop {
  0% {
    opacity: 1;
    transform: scale(0.6);
  }
  100% {
    opacity: 0;
    transform: scale(1.6);
  }
}
</style>

