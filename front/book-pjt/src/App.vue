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
            <RouterLink to="/books" class="nav-link">도서 목록</RouterLink>
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
            <RouterLink to="/profile" class="nav-link">내 책장</RouterLink>
          </div>

          <div class="dropdown">
            <RouterLink to="/challenge" class="nav-link">챌린지</RouterLink>
            <div class="dropdown-content">
              <ol>
                <li><RouterLink to="/challenge/list">챌린지 목록</RouterLink></li>
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
      <RouterView />
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
const logOut = () => store.LogOut();
const toggleMenu = () => (showMenu.value = !showMenu.value);

onMounted(() => {
  axios.post('http://127.0.0.1:8000/api/v1/books/import/')
    .then(res => console.log(res.data.message || '책 불러오기 완료'))
    .catch(err => console.error('책 불러오기 실패:', err));
});
</script>

<style scoped lang="scss">
:root {
  --dropdown-bg: #2B4570;
  --dropdown-hover-bg: #26456e; /* 완전 불투명 컬러 적용 */
  --submenu-bg: #EB8258;
}

.navbar {
  position: relative;
  z-index: 1000;
  background: #fff;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  overflow: visible;
}

.nav-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  overflow: visible;
}

.logo {
  font-size: 1.6rem;
  font-weight: bold;
  color: #222;
  text-decoration: none;
  z-index: 200;
}

.main-nav {
  display: flex;
  > .dropdown {
    position: relative;
    > .nav-link {
      position: relative;
      display: block;
      background-color: var(--dropdown-bg);
      color: #8b6060;
      padding: 16px;
      text-decoration: none;
      transition: background-color 200ms ease-out;
      &:nth-child(n+2) { border-left: 1px solid #fff; }
      z-index: 200;
    }
    > .dropdown-content {
      position: absolute;
      top: 100%;
      left: 0;
      display: none;
      z-index: 300;
      > ol {
        animation: dropdown 500ms forwards;
        margin: 0;
        padding: 0;
        list-style: none;
        background: var(--submenu-bg);
        border-radius: 2px;
        box-shadow: 0 2px 10px hsla(0, 0%, 0%, 0.25);
        overflow: hidden;
        > li {
          > a {
            display: block;
            padding: 10px 16px;
            color: #997676;
            text-decoration: none;
            font-size: 14px;
            white-space: nowrap;
            background-color: #fff;
            &:hover { background-color: hsl(0, 0%, 100%); }
          }
          &:nth-child(n+2) { border-top: 1px solid #fff; }
        }
      }
    }
    &:hover {
      > .nav-link { background-color: var(--dropdown-hover-bg); }
      > .dropdown-content { display: block; }
    }
  }
}

@keyframes dropdown {
  from { opacity: 0; transform: translateY(5px); }
  75% { opacity: 1; }
  to { transform: translateY(0); }
}

.actions {
  display: flex;
  gap: 12px;
  align-items: center;
  z-index: 2;
}
.actions a,
.actions button {
  background: none;
  border: none;
  color: #555;
  text-decoration: none;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 4px;
  transition: all 0.2s;
}

.actions button:hover,
.actions a:hover {
  color: var(--btn-bg);
}


.hamburger { 
 font-size: 1.5rem;
  background: none;
  border: none;
  display: none;
  cursor: pointer; }

@media (max-width: 768px) {
  .main-nav { 
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    display: none;
    flex-direction: column;
    background: #fff;
    border-bottom: 1px solid #ddd;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    max-height: calc(100vh - 60px);
    overflow-y: auto;
    z-index: 1000;
  }
  .main-nav.open .actions.mobile-actions { 
    display: flex; 
    flex-direction: column;
    background: #fff;
    border-top: 1px solid #ddd;
  }
  .hamburger { 
    display: block; 
    z-index: 1100;
  }
   .main-nav.open {
    display: flex;
  }
    /* 데스크탑 로그인/회원가입 숨김 */
  .actions.desktop-actions { 
    display: none !important; 
  }
  /* 모바일 메뉴 내 로그인/회원가입 표시 */
  .actions.mobile-actions {
    display: none;
  }
  .main-nav .nav-link {
    width: 100%;
    padding: 16px 24px;
    font-size: 1.1rem;
    border-bottom: 1px solid #f0f0f0;
  }

  /* 서브 메뉴는 접히도록 숨김 */
  .main-nav .dropdown-content {
    display: none !important;
  }
}
</style>
