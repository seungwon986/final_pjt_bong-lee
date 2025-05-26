<template>
  <div class="nav-wrapper">
    <nav class="navbar">
      <div class="container nav-container">

        <!-- 로고 -->
        <div class="left">
          <RouterLink to="/" class="logo">BookNest</RouterLink>
        </div>

        <!-- 중앙 메뉴 -->
        <div class="main-nav" :class="{ open: showMenu }">
          <div class="dropdown">
            <RouterLink to="/" class="nav-link">홈</RouterLink>
          </div>
          
          <div class="dropdown">
            <RouterLink to="/books" class="nav-link" exact-active-class="active">도서 목록</RouterLink>
            <div class="dropdown-content">
              <ol>
                <li><RouterLink :to="{ name: 'books', query: { category: '전체' } }">전체</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '인문' } }">인문</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '에세이' } }">에세이</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '만화' } }">만화</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '문학' } }">문학</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '사회과학' } }">사회과학</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '과학' } }">과학</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '예술' } }">예술</RouterLink></li>
                <li><RouterLink :to="{ name: 'books', query: { category: '기타' } }">기타</RouterLink></li>
              </ol>
            </div>
          </div>

          <div class="dropdown">
            <RouterLink to="/challenges" class="nav-link">챌린지</RouterLink>
            <div class="dropdown-content">
              <ol>
                <li><RouterLink to="/challenges">챌린지 목록</RouterLink></li>
                <li><RouterLink to="/challenge/create">챌린지 만들기</RouterLink></li>
              </ol>
            </div>
          </div>
          
          
        </div>

        <!-- 우측 메뉴 -->
         <div class="right">
           <div class="actions">
             <template v-if="store.isLogIn">
               <RouterLink to="/mypage" class="nav-link">마이 페이지</RouterLink>
               <button @click="logOut">로그아웃</button>
             </template>
             <template v-else>
               <RouterLink
                  to="/login"
                  class="nav-link"
                  active-class=""
                  exact-active-class=""
                >
                  로그인
                </RouterLink>
                <RouterLink
                  to="/signup"
                  class="nav-link"
                  active-class=""
                  exact-active-class=""
                >
                  회원가입
                </RouterLink>
             </template>
           </div>
          </div>



        <!-- 햄버거 메뉴 버튼 (모바일용) -->
        <button class="hamburger" @click="toggleMenu">☰</button>
      </div>
    </nav>

    <main class="main-wrapper">
      <transition name="fade" mode="out-in">
        <RouterView v-scroll-reveal />
      </transition>
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ScrollReveal from 'scrollreveal'

const store = useAccountStore()
const showMenu = ref(false)
const logOut = () => store.logOut()
const toggleMenu = () => (showMenu.value = !showMenu.value)

onMounted(() => {
  // ✅ 로그인 상태 유지 시 사용자 정보 불러오기
  if (store.token && !store.user) {
    store.fetchUserProfile()
  }

  axios
    .post('http://127.0.0.1:8000/api/v1/books/import/')
    .then(res => console.log(res.data.message || '책 불러오기 완료'))
    .catch(err => console.error('책 불러오기 실패:', err))

  axios
    .post("http://127.0.0.1:8000/api/v1/books/generate-vectors/")
    .then(() => console.log("✅ 벡터 생성 완료"))
    .catch((err) => console.error("❌ 벡터 생성 실패", err))

  ScrollReveal().reveal('[v-scroll-reveal]', {
    distance: '20px',
    origin: 'bottom',
    duration: 800,
    interval: 150,
    opacity: 0,
    easing: 'ease-out',
    reset: false,
  })
})
</script>


<style lang="scss">

.main-wrapper {
  width: 100%;
  max-width: none;     /* ✅ 중앙제한 제거 */
  padding: 0;          /* ✅ 좌우 여백 제거 */
}
:root {
  --dropdown-bg: transparent;
  --dropdown-hover-bg: rgba(0, 0, 0, 0.05);
  --submenu-bg: #fff;
  --accent-color: #4ef748;
}

body {
  font-family: 'Pretendard', sans-serif;
  font-weight: 400;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background: #fff;
  color: #222;
  overflow-x: hidden;
}



.navbar {
  width: 100%;
  background: #fff;
  box-shadow: none;
}
.nav-container {
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #000;
  justify-content: space-between;
}

.left {
  flex: 1;
}

.center {
  flex: 2;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #000;
  text-decoration: none;
}
/* 중앙 메뉴 */
.main-nav {
  display: flex;
  gap: 2rem;
  margin: 0 auto;

  .dropdown {
    position: relative;

    .nav-link {
      display: block;
      padding: 16px 20px;
      font-size: 0.95rem;
      font-weight: 500;
      color: #333;
      text-decoration: none;
      text-transform: uppercase;
      transition: all 0.3s ease;

      &:hover {
        background-color: rgba(0, 0, 0, 0.04);
        color: #000;
      }

      &.router-link-exact-active {
        color: #000;
        font-weight: 600;
        border-bottom: 2px solid var(--accent-color);
      }
    }

    .dropdown-content {
      position: absolute;
      top: 100%;
      left: 0;
      z-index: 300;
      visibility: hidden;
      opacity: 0;
      pointer-events: none;
      transform: translateY(8px);
      transition: all 0.3s ease;

      ol {
        list-style: none;
        margin: 0;
        padding: 0;
        background: var(--submenu-bg);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border-radius: 0.25rem;

        li a {
          display: block;
          padding: 10px 16px;
          color: #444;
          text-decoration: none;
          font-size: 0.9rem;
          transition: background 0.2s;

          &:hover {
            background: var(--dropdown-hover-bg);
            color: #000;
          }
        }
      }
    }

    &:hover .dropdown-content {
      visibility: visible;
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
  }
}
  .left {
    justify-content: flex-start;
  }

/* 인증 버튼 */
.actions {
  display: flex;
  justify-self: flex;
  gap: 16px;
  a,
  button {
    font-size: 0.9rem;
    color: #666;
    background: none;
    border: none;
    cursor: pointer;
    transition: color 0.2s ease;
    padding: 6px 10px;

    &:hover {
      color: var(--accent-color);
    }
  }
}

/* 햄버거 메뉴 (모바일용) */
.hamburger {
  display: none;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

/* 반응형 */
@media (max-width: 768px) {
  .hamburger {
    display: block;
  }

  .main-nav {
    display: none;
  }

  .main-nav.open {
    display: flex;
    flex-direction: column;
    background: #fff;
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    border-top: 1px solid #eee;
    z-index: 1000;
  }

  .main-nav.open .nav-link {
    width: 100%;
    padding: 16px 24px;
    border-bottom: 1px solid #f0f0f0;
  }

  .dropdown-content {
    display: none !important;
  }
}

/* 페이드 전환 효과 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

</style>
