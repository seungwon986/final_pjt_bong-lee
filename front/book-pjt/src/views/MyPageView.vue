<template>
  <div v-if="user" class="page-container">
    <div class="top-header">
    <h2 class="page-title">
      <img src="@/assets/house.png" class="title-icon" alt="house icon" />
      <span class="nickname-bold">{{ user.nickname }}</span>
      <span class="sub-label">님의 마이페이지</span>
    </h2>
    </div>

    <div class="mypage-dashboard">
      <!-- 사이드바 -->
      <aside class="sidebar">
       
          <div class="profile-edit-btn">
            <RouterLink to="/profile/edit" class="edit-icon">⚙️</RouterLink>
          </div>
          <img :src="imageUrl(user.profile_image)" alt="프로필" class="sidebar-avatar" />
          <p class="user-id">{{ user.nickname }}</p>
          <p class="follow-stats">
            <strong>팔로잉</strong> {{ user.following_count }}명
            <strong>팔로워</strong> {{ user.follower_count }}명
          </p>
      </aside>

      <!-- 메인 콘텐츠 -->
      <section class="main-content">
        

        <div class="all-sections-wrapper">

          <div class="card shelf-full-card">
            <div class="card-inner">
  
              <div class="shelf-header d-flex justify-content-between align-items-center">
                <h4>내 책장</h4>
                <RouterLink to="/books" class="bookmark-more-btn">➕ 더 많은 책 북마크 하기</RouterLink>
              </div>
              <div class="book-grid">
                <div class="book-card" v-for="book in preferredBooks" :key="book.id">
                  <img :src="book.cover || '/default-book-cover.png'" :alt="book.title" class="book-cover" />
                  <div class="book-info">
                    <div class="title-wrap">
                      <h3 class="book-title clamp">{{ book.title }}</h3>
                      <label class="heart-label">
                        <input type="checkbox" :checked="isLiked(book.id)" @change="togglePreferred(book.id)" class="heart-checkbox" />
                        <svg class="icon" viewBox="0 0 1024 1024">
                          <path class="heart-path"
                            d="M742.4 101.12A249.6 249.6 0 0 0 512 256a249.6
                               249.6 0 0 0-230.72-154.88C143.68 101.12 32 238.4
                               32 376.32c0 301.44 416 546.56 480 546.56s480-245.12
                               480-546.56c0-137.92-111.68-275.2-249.6-275.2z" />
                        </svg>
                        <span class="burst"></span>
                      </label>
                    </div>
                    <p class="book-author"> {{ book.author }}</p>
                    <!-- <p class="book-publisher"> {{ book.publisher }}</p>
                    <p class="book-date">{{ formattedDate(book.pub_date) }}</p>
                    <p class="book-description">{{ book.description }}</p> -->
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="card-row">
  
            <!-- 내가 쓴 글 (향후 확장) -->
            <div class="card info-card">
              <div class="card-inner">
                <h4>내가 쓴 글</h4>
                <p class="muted">게시글 카드 또는 리스트로 추가 예정</p>
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
          </div>
        </div>



      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts.js'
import defaultAvatar from '@/assets/basic.jpg'
import { RouterLink } from 'vue-router'




const store = useAccountStore()
const user = computed(() => store.user)
const joinedChallenges = ref([])
const preferredBooks = ref([])

const imageUrl = (path) => {
  if (!path) return defaultAvatar
  return path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`
}

const formattedDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}

const isLiked = (bookId) => store.user?.preferred_books.includes(bookId)

const fetchJoinedChallenges = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/challenges/my/', {
      headers: { Authorization: `Token ${store.token}` },
    })
    joinedChallenges.value = res.data
  } catch (err) {
    console.error('참여한 챌린지 로드 실패:', err)
  }
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
    console.error('선호 도서 정보 로드 실패:', err)
  }
}

const togglePreferred = async (bookId) => {
  const current = store.user?.preferred_books || []
  const updated = current.includes(bookId)
    ? current.filter(id => id !== bookId)
    : [...current, bookId]

  try {
    await axios.patch('http://127.0.0.1:8000/accounts/profile/', {
      preferred_books: updated,
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })
    await store.fetchUserProfile()
    await fetchJoinedChallenges()
    await fetchPreferredBooks()
  } catch (err) {
    console.error('북마크 저장 실패:', err)
  }
}

onMounted(async () => {
  await store.fetchUserProfile()
  await fetchJoinedChallenges()
  await fetchPreferredBooks()
})
</script>

<style scoped>
* {
  font-family: 'AritaM';
}
:root {
  --sidebar-width: 220px;  /* .sidebar { flex: 0 0 220px; } 에 맞춰줍니다 */
  --layout-gap: 2rem;      /* .mypage-dashboard { gap: 2rem; } 과 동일하게 */
}
.main-content .card,
.main-content .shelf-full-card {
  border: none !important;
}
h4 {
    margin-left: 20px;              /* 제목 밑의 마진 제거 */
  margin-top: 20px;   
  color: #414040;
}
.card-inner p {
    margin-left: 20px;              /* 제목 밑의 마진 제거 */
  margin-top: 20px;   
}
.top-header {
  height: auto;
  padding-top: 1rem;
}
.page-container {
    display: flex;
  flex-direction: column;
  background: #ddf1ddb4;      /* 전체를 연한 회색톤으로 */
  border-radius: 1.5rem;
  padding: 4rem 2rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  max-width: 1400px;
  margin: 3rem auto;
}
.mypage-dashboard {
  display: flex;
  gap: 2rem;
  align-items: flex-start; /* 기본적으로 왼쪽 위 정렬 */


}
.main-content { flex:1 }
.sidebar {
  flex: 0 0 220px;
  background-color: #ffffff;  
  margin-top: 3.5rem; /* .page-title의 높이만큼 내려줍니다 */
  border-radius: 1rem 1rem 1rem 1rem;
  padding: 2rem;
  margin-top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}
.profile-edit-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #6cecc0a6;
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
  border: 2px solid #ffffff;  
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}
.user-id {
  margin-top: 1rem;
  font-size: 1.125rem;
  font-weight: 500;
  color: #34495e;    
}
.follow-stats {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}
.follow-stats strong {
  color: #2c3e50;
}
.main-content {
  flex: 1;
  display: block;
}
.page-title {
    display: inline-block;   /* 배경색이 텍스트만 감싸도록 */

  border-radius: 0.5rem;
  padding: 0.5rem 15rem;
  margin-left: calc(var(--sidebar-width) + var(--layout-gap));
  font-size: 2rem;
  font-weight: 700;
  justify-self: center;
  background-color: transparent;
    color: #2c3e50; 
  border-radius: 20%;
  margin-bottom: 2rem;
    width: auto !important;


}

.page-title .nickname-bold {
  font-size: 1.6rem;
  text-shadow: 1px 1px 2px rgba(20, 20, 20, 0.2);
}
.page-title .sub-label {
  font-size: 1.3rem;
}
.page-title .title-icon {
  width: 70px;
  height: 70px;
  margin-right: 0.5rem;
  vertical-align: middle;
  object-fit: contain;
  
}

.calendar-widget {
  margin-top: 2rem;
  width: 100%;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.75rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.shelf-header {
  margin-bottom: 0;       /* 기본 margin 제거 */
  padding-bottom: 0.5rem; /* 원하시는 만큼만 여백 유지 */
}
.shelf-header h4 {
  margin-left: 20px;              /* 제목 밑의 마진 제거 */
  margin-top: 20px;              /* 제목 밑의 마진 제거 */


}
.shelf-full-card {
  display: flex;
  justify-content: space-between;
  align-content: center;
  background: #ffffff;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.03);
  margin-bottom: 2rem;
  width: 100%;
}
/* 북마크 더보기 버튼 */
.bookmark-more-btn {
  font-size: 0.9rem;
  padding: 0.4rem 0.8rem;
  margin-right: 10px;
  background-color: #2cd99c;
  color: white;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background 0.2s;
}
/* 모바일 제외, 모든 크기에서 그리드 */
.shelf-full-card .book-grid {
  display: grid !important;
  /* 카드 최소 너비 250px, 화면에 꽉 차면 1fr씩 늘어납니다 */
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)) !important;
  gap: 1rem !important;
}
.shelf-full-card .book-card {
  /* flex 속성이 방해하니 해제 */
  flex: unset !important;
  width: 100%;
}
.book-grid {
  display: grid;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0;
  grid-template-columns: repeat(5, 1fr);
  justify-content: flex-start;
}
/* 🟢 책 카드 그리드 */
.book-grid.horizontal-scroll {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  height: 250px;
}
/* 🟢 카드 공통 스타일 */
.card {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.shelf-full-card {
  margin-bottom: 2rem;

}
.card-row {
  gap: 1rem;
}
.card h4 {
  font-family: 'AritaB';
}
.card-inner {
  padding-top: 0.5rem;
  padding-bottom: 1rem;
  border-radius: 0.75rem;
  box-sizing: border-box;
  flex-grow: 1;
  height: 100%;
}

/* 🟢 글/챌린지 카드 나란히 */
.card-row {
  display: flex;
  gap: 2rem;
  align-items: stretch;
  margin-bottom: 2rem;
}
.card-row > .card {
  flex: 1;
  display: flex;
  flex-direction: column;
}


.book-card {
  max-width: 160px;
  margin: 0 auto;
    background: #ffffff;   
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.book-cover:hover {
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  transform: translateY(-6px);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.book-cover {
  width: 100%;
  height: auto;           /* 높이 자동 */
  object-fit: contain;    /* 온전한 비율 유지 */
  border-radius: 0.5rem;  /* 원하는 만큼 모서리 둥글게 */
}
.book-info {
  padding: 0.5rem 0;
  text-align: center;
}
.title-wrap {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.book-title {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
    color: #2c3e50;
}
.book-author {
  font-size: 0.75rem;
  color: #666;
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
  width: 20px;
  height: 20px;
  margin-left: 8px;
}
.heart-checkbox {
  display: none;
}
.icon {
  width: 15px;
  height: 15px;
  fill: none;
  stroke: #c91a7a;
  stroke-width: 100px;
  transition: stroke 0.3s ease;
  z-index: 2;
  position: relative;
}
/* 기본: outline 하트 */
.icon .heart-path {
  fill: none;
  stroke: #e25555;
  stroke-width: 2;
  transition: fill 0.2s, stroke 0.2s;
}
/* 체크(좋아요) 상태일 때: 하트 채우기 */
.heart-checkbox:checked + .icon .heart-path {
  fill: #e25555;
  stroke: #e25555;
}
/* scoped 안에서 burst 효과 활성화 */
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
/* 🟢 반응형 (모바일 대응) */
@media (max-width: 768px) {
  .mypage-dashboard {
    flex-direction: column;
  }
  .sidebar {
    background-color: #bbcfc891;
    width: 100%;
    margin-bottom: 2rem;
  }
  .card-row {
    flex-direction: column;
  }
  .bookmark-more-btn {
    font-size: 0.8rem;
    padding: 0.3rem 0.6rem;
    max-width: 160px;
  }
    .shelf-full-card .book-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 1rem;
  }

  /* 2) 카드 flex 해제, 그리드 전담 */
  .shelf-full-card .book-card {
    flex: unset !important;
    width: 100%;
  }

  /* 3) 표지 비율 유지 */
  .shelf-full-card .book-cover {
    height: auto !important;
    aspect-ratio: 3 / 4;
  }
  }
  
@media (max-width: 1024px) {
  .book-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ── 3. 작은 화면: 모바일 (2열) ── */
@media (max-width: 600px) {
  .book-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
.nickname-bold {
  font-weight: 800;
  font-size: 2.2rem;
  color: #2c3e50;
}

.sub-label {
  font-weight: 400;
  font-size: 1.5rem;
  margin-left: 0.2rem;
  color: #34495e;
}


.fullcalendar-wrapper {
  width: 100%;
  max-width: 200px;    /* 원하는 너비로 줄이기 */
  font-size: 0.7rem;   /* 전체 글씨 크기 축소 */
  overflow: hidden;
}

:deep(.fc) {
  font-size: 0.75rem;
}

:deep(.fc-toolbar-title) {
  font-size: 1rem;
}

:deep(.fc-button) {
  padding: 0.2rem 0.4rem;
  font-size: 0.7rem;
  height: 1.5rem;
}

</style>
