




<template>
  <div id="nav">
    <nav class="navbar">
      <div class="container nav-container">
        <!-- 로고 -->
        <RouterLink to="/" class="logo">BookNest</RouterLink>

        <!-- 중앙 메뉴 -->
        <nav class="main-nav open-line" :class="{ open: showMenu }">
          <RouterLink to="/">홈</RouterLink>
          <RouterLink to="/books">도서 목록</RouterLink>

          <RouterLink to="/mybooks">내 책장</RouterLink>

          <RouterLink to="/challenge">챌린지</RouterLink>
          <RouterLink to="/community">커뮤니티</RouterLink>
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
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/accounts.js";

import { ref, onMounted } from "vue";
import axios from "axios";


const store = useAccountStore();
const showMenu = ref(false);

const logOut = () => {
  store.logOut();
};

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

// 책 자동 불러오기 (초기 렌더링 시)
onMounted(() => {
  axios
    .post("http://127.0.0.1:8000/api/v1/books/import/")
    .then((res) => {
      console.log(res.data.message || "책 불러오기 완료");
    })
    .catch((err) => {
      console.error("책 불러오기 실패:", err);
    });
});

onMounted(() => {
  axios
    .post("http://127.0.0.1:8000/api/v1/books/generate-vectors/")
    .then(() => console.log("✅ 벡터 생성 완료"))
    .catch((err) => console.error("❌ 벡터 생성 실패", err));
});
</script>

<style scoped lang="scss">
:root {
  --btn-bg: #fc47b0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}


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


.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #222;
  text-decoration: none;
  z-index: 2;
}


.main-nav {
  display: flex;
  gap: 24px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;

  a {
    position: relative;
    color: #333;
    text-decoration: none;
    padding: 8px 0;
    transition: color 0.2s, letter-spacing 0.3s;

    &::before,
    &::after {
      content: "";
      position: absolute;
      left: 0;
      width: 100%;
      height: 1px;
      background: var(--btn-bg);
      opacity: 0;
      transform: scaleX(0);
      transition: 0.4s ease-in-out;
    }


    &::before {
      top: 0;
    }
    &::after {
      bottom: -2px;
    }


    &:hover {
      letter-spacing: 0.1em;
      color: var(--btn-bg);
      &::before,
      &::after {
        opacity: 1;
        transform: scaleX(1.2);
      }
    }

    &.active {
      color: var(--btn-bg);
      font-weight: 600;

      &::after {
        content: "";
        position: absolute;
        left: 0;
        bottom: -2px;
        width: 100%;
        height: 4px;
        background-color: var(--btn-bg);
        border-radius: 2px;
      }
    }
  }
}

.actions {
  position: absolute;
  right: 24px;
  display: flex;
  gap: 16px;
  align-items: center;
  z-index: 2;


  a,
  button {

  a, button {

    background: none;
    border: none;
    color: #555;
    text-decoration: none;
    font-size: 0.9rem;
    cursor: pointer;
    padding: 6px 0;

    &:hover {
      color: #000;
    }
  }
}


.hamburger {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 3;
}


@media (max-width: 768px) {
  .main-nav {
    display: none;
    flex-direction: column;
    background: #fff;
    position: absolute;
    top: 100%;
    left: 24px;
    right: 24px;
    padding: 8px 0;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }

  .main-nav.open {
    display: flex;
  }

  .hamburger {
    display: block;
  }
}
</style>

