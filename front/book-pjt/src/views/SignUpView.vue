<template>
  <div class="panel shadow1">
    <form @submit.prevent>
      <!-- 진행 단계 바 -->
      <div class="progress-bar animate4">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="progress-dot"
          :class="{ active: index <= currentStep }"
        ></div>
      </div>
      <h1 class="animate1">회원가입</h1>
      
      <!-- 회원가입 단계별 컴포넌트 렌더링 -->
      <div class="animate2 step-panel">
        <component
          :is="steps[currentStep]"
          :form="form"
          @next="nextStep"
          @prev="prevStep"
        />
      </div>

      <!-- 다음 단계로 넘어가는 버튼 -->
      
    </form>
    <div class="panel-switch animate3">
      <button v-if="currentStep > 0" type="button" class="nav-btn prev" @click="prevStep">이전</button>
      <button
        v-if="currentStep < steps.length - 1"
        type="button"
        class="nav-btn next"
        @click="nextStep"
      >다음</button>
      <button
        v-if="currentStep === steps.length - 1"
        type="submit"
        class="nav-btn submit"
      >회원가입 완료</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

import SignUpStep1 from '@/components/signup/SignUpStep1.vue'
import SignUpStep2 from '@/components/signup/SignUpStep2.vue'
import SignUpStep3 from '@/components/signup/SignUpStep3.vue'
import SignUpStep4 from '@/components/signup/SignUpStep4.vue'

const form = ref({
  username: '',
  password1: '',
  password2: '',
  nickname: '',
  first_name: '',
  last_name: '',
  gender: '',
  birth: '',
  profile_image: null,
  preferred_categories: [],
  preferred_books: [],
})

const steps = [SignUpStep1, SignUpStep2, SignUpStep3, SignUpStep4]
const currentStep = ref(0)

const nextStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}
</script>

<style scoped>
.panel {
  width: 600px;
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

input,
select {
  padding: 10px 14px;
  font-size: 14px;
  border-radius: 12px;
  border: 1px solid #ccc;
}

h1.animate1 {
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
