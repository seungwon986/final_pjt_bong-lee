<template>
  <div v-if="user" class="page-container">
    <div class="mypage-dashboard">
      <aside class="sidebar">
        <div class="profile-edit-btn">
          <RouterLink to="/profile/edit" class="edit-icon">⚙️</RouterLink>
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
  }
}

const togglePreferred = async (bookId) => {
  const current = store.user?.preferred_books || []
  const updated = current.includes(bookId)
    ? current.filter(id => id !== bookId)
    : [...current, bookId]

  try {
    await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      preferred_books: updated
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })
    await store.fetchUserProfile()
    await fetchLikedBooks()
  } catch (err) {
    console.error('북마크 저장 실패:', err)
  }
}

onMounted(async () => {
  await store.fetchUserProfile()
  fetchJoinedChallenges()
  await fetchLikedBooks()
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
</style>
