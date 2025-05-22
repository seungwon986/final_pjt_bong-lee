<template>
  <div class="signup-page">
    <div class="stepper">
      <div
        v-for="(item, index) in stepItems"
        :key="index"
        class="step"
        :class="{ completed: currentStep > index, active: currentStep === index }"
      >
        <div class="step-circle">
          <span class="material-icons">{{ item.icon }}</span>
        </div>
        <div class="step-label">{{ item.label }}</div>
      </div>
    </div>

    <div class="form-container">
      <h2>회원가입</h2>
      <component
        :is="steps[currentStep]"
        v-model:user="user"
        v-model:selectedCategories="selectedCategories"
        v-model:selectedBooks="selectedBooks"
        @next="currentStep++"
        @prev="currentStep--"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SignUpStep1 from '@/components/signup/SignUpStep1.vue'
import SignUpStep2 from '@/components/signup/SignUpStep2.vue'
import SignUpStep3 from '@/components/signup/SignUpStep3.vue'
import SignUpStep4 from '@/components/signup/SignUpStep4.vue'

const currentStep = ref(0)
const steps = [SignUpStep1, SignUpStep2, SignUpStep3, SignUpStep4]

const user = ref({})
const selectedCategories = ref([])
const selectedBooks = ref([])

const stepItems = [
  { label: '기본정보', icon: 'person' },
  { label: '선호 카테고리', icon: 'category' },
  { label: '선호 도서 선택', icon: 'menu_book' },
  { label: '정보 확인', icon: 'check_circle' }
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
.form-container h2 {
    text-align: center;
    margin-bottom: 40px;
}
.signup-page {
  position: absolute;
  width: 100%;
  min-height: 100vh;
  background: #f9f9f9;
  padding-top: 140px; /* 스텝바 전체 높이 + 여유 */
}

.stepper {
  margin-top: 30px;
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  width: 90%;
  max-width: 600px;
  align-items: flex-start; /* 서클 기준으로 상단 정렬 */
  z-index: 10;
  background: transparent;
  padding: 20px 0;
}

.step {
  position: relative;
  flex: 1;
  text-align: center;
  z-index: 1;
  padding-top: 10px; /* 라벨과 서클 간격 조절 */
}

.step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 20px; /* 서클 중심 높이(서클 40px 기준) */
  left: calc(50% + 20px);
  width: calc(100% - 40px);
  height: 2px;
  background: #e0e0e0;
  z-index: 0;
}

.step.completed::after {
  background: #1677FF;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  transition: background 0.3s, color 0.3s;
}

.step.completed .step-circle,
.step.active .step-circle {
  background: #1677FF;
  color: #fff;
}

.step-label {
  margin-top: 8px;
  font-size: 0.9em;
  color: #777;
  white-space: nowrap;
  transition: color 0.3s;
}

.step.completed .step-label,
.step.active .step-label {
  color: #1677FF;
  font-weight: 600;
}

.form-container {
  margin: 0 auto;
  width: 90%;
  max-width: 600px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.form-container .form-group {
  margin-bottom: 20px;
}

.form-container label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-container input,
.form-container select,
.form-container textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1em;
}

.btn-signup {
  width: 100%;
  padding: 14px;
  margin-top: 30px;
  background: #1677FF;
  color: #fff;
  font-size: 1.1em;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-signup:hover {
  background: #005fcc;
}

@media (max-width: 480px) {
  .stepper {
    flex-wrap: wrap;
  }
  .step-label {
    display: none;
  }
  .step:not(:last-child)::after {
    display: none;
  }
}
</style>