<template>

  <div v-if="user" class="page-container">
    <div class="mypage-dashboard">
      <aside class="sidebar">
        <div class="profile-edit-btn">
          <RouterLink to="/profile/edit" class="edit-icon">⚙️</RouterLink>

  <div v-if="user" class="container py-4">
    <h2 class="mb-4">📖 마이페이지</h2>

    <!-- 프로필 -->
    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="border p-2 text-center">
          <img :src="imageUrl(user.profile_image)" alt="프로필" class="img-fluid rounded" />
          <p class="mt-2 fw-semibold">{{ user.nickname }}</p>

        </div>
        <img :src="imageUrl(user.profile_image)" alt="프로필" class="sidebar-avatar" />
        <p class="user-id">{{ user.username }}</p>
        <p class="follow-stats">
          <strong>팔로잉</strong> {{ user.following_count }}명
          <strong>팔로워</strong> {{ user.follower_count }}명
        </p>
      </aside>

      <section class="main-content">
        <h2 class="page-title">
          <img src="@/assets/house.png" class="title-icon" alt="house icon" /> {{ user.nickname }}님의 마이페이지
        </h2>

        <!-- 내 책장 -->
        <div class="card shelf-full-card">
          <div class="card-inner">
            <div class="shelf-header">
              <h4>내 책장</h4>
              <RouterLink to="/books" class="bookmark-more-btn">➕ 더 많은 책 북마크 하기</RouterLink>
            </div>


            <div class="book-grid horizontal-scroll">
              <BookCard
                v-for="book in mergedBooks"
                :key="book.id"
                :book="book"
                :is-preferred="user.preferred_books.includes(book.id)"
                @toggle-preferred="togglePreferred"
              />
            </div>
          </div>
        </div>

        <!-- 내가 쓴 글 -->
        <div class="card info-card">
          <div class="card-inner">
            <h4>내가 쓴 글</h4>
            <p class="muted">게시글 카드 or 리스트 삽입 예정</p>
          </div>
        </div>

        <!-- 참여한 챌린지 -->
        <div class="card challenge-card">
          <div class="card-inner">
            <h4>참여한 챌린지</h4>
            <ul class="list">
              <li v-for="challenge in joinedChallenges" :key="challenge.id">
                {{ challenge.title }} ({{ challenge.participants.length }}명 참여)
              </li>
            </ul>

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
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'

import BookCard from '@/components/BookCard.vue'
import defaultAvatar from '@/assets/basic.jpg'
import { RouterLink } from 'vue-router'

const store = useAccountStore()
const user = computed(() => store.user)
const joinedChallenges = ref([])
const likedBooks = ref([])
const mergedBooks = computed(() => likedBooks.value)

const imageUrl = path => {
  return path ? (path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`) : defaultAvatar
}

const fetchJoinedChallenges = async () => {
  const res = await axios.get('http://127.0.0.1:8000/api/v1/challenges/my/', {
    headers: { Authorization: `Token ${store.token}` }
  })
  joinedChallenges.value = res.data
}

const fetchLikedBooks = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/books/favorites/', {
      headers: { Authorization: `Token ${store.token}` }
    })
    likedBooks.value = res.data
  } catch (err) {
    console.error('좋아요 도서 로드 실패:', err)


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

  const current = store.user?.preferred_books || []
  const updated = current.includes(bookId)
    ? current.filter(id => id !== bookId)
    : [...current, bookId]

  try {
    const current = store.user?.preferred_books || []
    const updated = current.includes(bookId)
      ? current.filter((id) => id !== bookId)
      : [...current, bookId]


  try {
    await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      preferred_books: updated,
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })
    await store.fetchUserProfile()

    await fetchLikedBooks()

    await fetchPreferredBooks()

  } catch (err) {
    console.error('북마크 저장 실패:', err)
  }
}

onMounted(async () => {
  await store.fetchUserProfile()

  fetchJoinedChallenges()
  await fetchLikedBooks()
  await fetchPreferredBooks()

})
</script>

<style scoped>

.page-container {
  background: #c2f89e8c;
  border-radius: 1.5rem;
  padding: 4rem 2rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  margin: 3rem 2rem;
}
.mypage-dashboard {
  display: flex;
  gap: 2rem;
}
.sidebar {
  flex: 0 0 220px;
  background: #fff;
  border-radius: 1.5rem 0 1rem 1rem;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  
}
.profile-edit-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #2cd99c;
  width: 32px;
  height: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.15);
  z-index: 10;
}
.edit-icon {
  font-size: 18px;
  color: white;
  text-decoration: none;
}
.sidebar-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;

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
  border: 3px solid #e2fbef;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}
.user-id {
  margin-top: 1rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #2c3e50;
}
.follow-stats {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}
.follow-stats strong {
  color: #2c3e50;
}
.main-content {
  flex: 1;
}
.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 2rem;
}
.page-title .title-icon {
  width: 80px;   /* 적당한 크기로 지정 */
  height: 80px;
  margin-right: 0.5rem;
  vertical-align: middle;
  object-fit: contain;
}
.shelf-full-card {
  background: #fff;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}
.bookmark-more-btn {
  font-size: 0.9rem;
  padding: 0.4rem 0.8rem;
  background-color: #2cd99c;
  color: white;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background 0.2s;
}
.book-grid.horizontal-scroll {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  height: 250px;
}
.card {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
}
.card:hover {
  /* transform: translateY(-5px); */
}
.card-inner {
  background-color: #fefefe;
  padding: 1rem;
  border-radius: 0.75rem;
  box-sizing: border-box;
  flex-grow: 1;
}
.info-card h4,
.challenge-card h4 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #2c3e50;
}
.muted {
  color: #7f8c8d;
  font-size: 0.95rem;
}
.list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.list li {
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
  font-size: 1rem;
  color: #34495e;
}
.content-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}
@media (max-width: 960px) {
  .mypage-dashboard {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
  }
  .content-grid {
    grid-template-columns: 1fr;
  }
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

