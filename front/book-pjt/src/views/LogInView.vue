<!-- views/SignUpView.vue -->

<template>
  <div class="login-container">
    <form @submit.prevent="onLogIn">
      <label for="username">Username: </label>
      <input type="text" id="username" v-model="username" />
      <br />
      <label for="password1">Password: </label>
      <input type="password" id="password" v-model="password" />
      <br />
      <input type="submit" value="로그인" />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/accounts.js";
const store = useAccountStore();
const username = ref("");
const password = ref("");

const onLogIn = function () {
  const info = {
    username: username.value,
    password: password.value,

  };
  store.logIn(info)
};
</script>

<style>
/* 1) 전체 레이아웃: 좌우 분할, 100vh */
.login-container {
  position: relative;
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 2) 오른쪽 배경: 그라디언트 + 곡선 마스크 */
.login-container::after {
  content: "";
  position: absolute;
  top: 0; right: 0;
  width: 60%;
  height: 100%;
  background: linear-gradient(135deg, #A8E063, #56AB2F);
  /* 중앙에서 둥근 곡선 처리 */
  clip-path: circle(150% at 0% 50%);
  z-index: 1;
}

/* 3) 폼 스타일: 왼쪽 하얀 박스 */
.login-container form {
  position: relative;
  z-index: 2;
  width: 360px;
  margin: auto 0 auto 10%;
  padding: 40px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 4) 제목 */
.login-container form h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
  text-align: center;
}

/* 5) 라벨 */
.login-container form label {
  font-size: 0.9rem;
  color: #555;
}

/* 6) 입력 필드 */
.login-container form input[type="text"],
.login-container form input[type="password"] {
  padding: 12px 16px;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 999px;
  outline: none;
  transition: border-color 0.2s;
}
.login-container form input:focus {
  border-color: #56AB2F;
}

/* 7) 버튼 */
.login-container form button {
  margin-top: 10px;
  padding: 12px;
  font-size: 1rem;
  color: #fff;
  background: #56AB2F;
  border: none;
  border-radius: 999px;
  cursor: pointer;
}
.login-container form button:hover {
  background: #4a8e30;
}

/* 8) 반응형: 모바일에서는 곡선 뒷배경과 폼이 세로 배열 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }
  .login-container::after {
    /* 위쪽 절반만 배경 */
    clip-path: circle(150% at 50% 100%);
    width: 100%;
    height: 50%;
  }
  .login-container form {
    margin: 20px auto;
    width: 90%;
  }
}
</style>
