<template>
  <div>
    <nav class="navbar">
      <div class="container">
        <!-- 로고 -->
        <RouterLink to="/" class="logo">BookNest</RouterLink>
  
        
        
        <!-- 중앙 메뉴 -->
        <nav :class="['main-nav', { open: showMenu }]">
          <RouterLink to="/" exact-active-class="active">홈</RouterLink>
          <RouterLink to="/books" active-class="active">도서 목록</RouterLink>
          <RouterLink to="/profile" active-class="active">내 책장</RouterLink>
          <RouterLink to="/challenge" active-class="active">챌린지</RouterLink>
          <RouterLink to="/community" active-class="active">커뮤니티</RouterLink>
        </nav>      
        
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
      </div>
      
      
      <button class="menu-btn" @click="showMenu = !showMenu">
      <!-- 간단히 텍스트로, 아이콘 폰트나 SVG로 대체 가능 -->
        ☰
      </button>
    </nav>

    <main class="container">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/accounts.js";
import { onMounted } from 'vue'
import axios from 'axios'

const store = useAccountStore();
const logOut = function () {
  store.LogOut();
};
onMounted(() => {
  axios.post('http://127.0.0.1:8000/api/v1/books/import/')
    .then(res => {
      console.log(res.data.message || '책 불러오기 완료')
    })
    .catch(err => {
      console.error('책 불러오기 실패:', err)
    })
})
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Nav 바 ── */
.navbar {
  margin-top: 20px;
  padding-bottom: 20px;
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
}
.nav-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

/* 로고 */
.logo {
  position: absolute;
  left: 24px;
  font-size: 1.5rem;
  font-weight: 700;
  color: #222;
  text-decoration: none;
  z-index: 2;
}

/* 중앙 메뉴 (데스크탑) 절대위치*/
.main-nav {
  display: flex;
  gap: 24px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 24px;
  z-index: 1;
}
.main-nav a {
  position: relative;    /* ::after 위치 기준 */
  color: #333;
  text-decoration: none;
  padding: 8px 0;        /* 언더라인 여유 확보 */
  transition: color 0.2s;
}
.main-nav a:hover,
.main-nav a.active {
  color: #000;
  font-weight: 600;
}
.main-nav a.active {
  color: #fc47b0;        /* 언더라인과 같은 색 */
  font-weight: 600;      /* 강조용 굵기 */
}
.main-nav a.active::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;          /* 텍스트 아래 약간 떨어뜨려서 */
  width: 100%;
  height: 4px;           /* pill 두께 */
  background-color: #fc47b0;
  border-radius: 2px;     /* pill 끝 둥글게 */
}
/* 우측 버튼 */
.actions {
  position: absolute;
  right: 24px;
  display: flex;
  gap: 16px;
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
  padding: 6px 0;
}
.actions a:hover,
.actions button:hover {
  color: #000;
}

/* 햄버거 버튼 – 데스크톱에선 숨김 */
.hamburger {
  position: absolute;
  right: 24px;
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 3;
}

/* ── 반응형(<=768px) ── */
@media (max-width: 768px) {
  /* 숨기기 */
  .main-nav {
    display: none;
    flex-direction: column;
    background: #fff;
    position: absolute;
    top: 100%;
    left: 24px;
    right: 24px;
    padding: 8px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    border-radius: 4px;
  }
  /* 열렸을 때 */
  .main-nav.open {
    display: flex;
  }
  /* 햄버거 보이기 */
  .hamburger {
    display: block;
  }
}
</style>
