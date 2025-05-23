<template>
  <div class="panel shadow1">
    <form @submit.prevent="onLogIn">
      <!-- 제목 -->
      <h1 class="animate1">로그인</h1>

      <!-- 아이디 입력 -->
      <fieldset>
        <input
          type="text"
          id="username"
          placeholder="아이디"
          v-model="username"
          required
          class="animate2"
        />
      </fieldset>

      <!-- 비밀번호 입력 -->
      <fieldset>
        <input
          type="password"
          id="password"
          placeholder="비밀번호"
          v-model="password"
          required
          class="animate3"
        />
      </fieldset>

      <!-- 로그인 버튼 -->
      <button type="submit" class="nav-btn next animate4">로그인</button>

      <!-- 회원가입 링크 -->
      <p class="animate4" style="text-align:center; margin-top: 16px;">
        <RouterLink to="/signup">아직 회원이 아니신가요?</RouterLink>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from '@/stores/accounts.js';
import { RouterLink } from 'vue-router';

const store = useAccountStore();
const username = ref('');
const password = ref('');

function onLogIn() {
  const info = { username: username.value, password: password.value };
  store.logIn(info);
}
</script>

<style scoped>
.panel {
  width: 400px;
  margin: 60px auto;
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;

}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: auto;
  overflow: visible;
   align-items: center; 
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.shadow1 {
  animation: slideUpFadeIn 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(30px);
}
@keyframes slideUpFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

input ,
select {
  width: 100%;
  padding: 10px 14px;
  font-size: 14px;
  border-radius: 12px;
  border: 1px solid #ccc;
}

h1.animate1 {
  justify-content: center;
  padding-top: 30px;
  padding-bottom: 60px;
  font-size: 28px;
  font-weight: bold;
  color: #444;
  text-align: center;
  margin-bottom: 12px;
}
.step-panel {
  margin-top: 16px;
  animation: fadeIn 0.4s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.panel-switch {
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

/* 이전, 다음버튼 */
.nav-btn {
  margin-top: 60px;
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* 이전버튼 회색바탕, 검정글자 */
.prev {
  background-color: #ccc;
  color: #333;
}
.prev:hover {
  background-color: #bbb;
}

/* 다음버튼 */
.next {
  background-color: #f796ce;
  color: white;
}
.next:hover {
  background-color: #e23f9e;
}

.submit {
  background-color: #4caf50;
  color: white;
}
.submit:hover {
  background-color: #3e9e44;
}
.progress-bar {
  display: flex;
  justify-content: center;
  flex-direction: row !important; 
  align-items: center;
  gap: 12px;
  animation: fadeIn 0.5s ease-in-out;
}

.progress-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background-color: #ddd;
  transition: background-color 0.3s ease;
}
.progress-dot.active {
  background-color: #fc47b0;
}

</style>
