<template>
  <div id="nav">
    <nav class="navbar">
      <div class="container nav-container">
        <!-- 로고 -->
        <RouterLink to="/" class="logo">BookNest</RouterLink>

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
          
          <div class="dropdown">
            <RouterLink to="/community" class="nav-link">커뮤니티</RouterLink>
          </div>
        </div>

        <!-- 우측 메뉴 -->
         
       <div class="actions">
          <template v-if="store.isLogIn">
            <RouterLink to="/mypage" class="nav-link">마이 페이지</RouterLink>
            <button @click="logOut">로그아웃</button>
          </template>
          <template v-else>
            <RouterLink to="/login">로그인</RouterLink>
            <RouterLink to="/signup">회원가입</RouterLink>
          </template>
        </div>


        <!-- 햄버거 메뉴 버튼 (모바일용) -->
        <button class="hamburger" @click="toggleMenu">☰</button>
      </div>
    </nav>

    <main class="container py-4">
  <transition name="fade" mode="out-in">
    <RouterView />
  </transition>
</main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useAccountStore } from '@/stores/accounts.js';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const store = useAccountStore();
const showMenu = ref(false);
const logOut = () => store.logOut();
const toggleMenu = () => (showMenu.value = !showMenu.value);

onMounted(() => {
  axios.post('http://127.0.0.1:8000/api/v1/books/import/')
    .then(res => console.log(res.data.message || '책 불러오기 완료'))
    .catch(err => console.error('책 불러오기 실패:', err));
});
</script>

<style lang="scss">


body {
  font-family: 'Pretendard', sans-serif;
  font-weight: 400;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background: #fff;
  color: #222;
}

:root {
  --dropdown-bg: transparent;
  --dropdown-hover-bg: rgba(0, 0, 0, 0.05);
  --submenu-bg: #fff;
  --accent-color: #4ef748;
}

.navbar {
  background: #fff;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #000;
  text-decoration: none;
}

.main-nav {
  display: flex;
  gap: 1rem;

  > .dropdown {
    position: relative;

    > .nav-link {
      position: relative;
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

    > .dropdown-content {
      position: absolute;
      top: 100%;
      left: 0;
      z-index: 300;
      display: none;
      transform: translateY(8px);
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s ease;

      > ol {
        list-style: none;
        margin: 0;
        padding: 0;
        background: var(--submenu-bg);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border-radius: 0.25rem;

        > li > a {
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

    &:hover > .dropdown-content {
      display: block;
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
  }
}

.actions {
  display: flex; /* ✅ 버튼들을 가로로 정렬 */
  gap: 16px;     /* ✅ 버튼 사이 간격 */
  align-items: center; /* ✅ 세로 중앙 정렬 */
  right: 24px;
  z-index: 2;

  a,
  button {
    font-size: 0.9rem;
    vertical-align: middle;
    padding: 6px 10px;
    color: #666;
    background: none;
    border: none;
    cursor: pointer;
    transition: color 0.2s ease;

    &:hover {
      color: var(--accent-color);
    }
  }
}


.hamburger {
  display: none;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

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
.nav-link.active {
  border-bottom: 2px solid var(--accent-color);
  color: #000;
  font-weight: 600;
}

/* 화면 전환 페이드 효과 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px); /* 밑에서 살짝 올라오는 느낌 */
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

</style>