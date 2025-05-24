<template>
  <div class="panel shadow1">
    <form @submit.prevent="submitForm">
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
          @submit="submitForm"
        />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
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
const store = useAccountStore()
const router = useRouter()

const submitForm = async () => {
  const {
    username, password1, password2, nickname, first_name, last_name,
    gender, birth, preferred_categories, preferred_books, profile_image
  } = form.value

  if (!username || !password1 || !password2 || !nickname || !first_name || !last_name || !gender || !birth || !preferred_categories.length || !preferred_books.length) {
    alert('모든 항목을 올바르게 입력했는지 확인해주세요.')
    return
  }

  const data = new FormData()
  data.append('username', username)
  data.append('password1', password1)
  data.append('password2', password2)
  data.append('nickname', nickname)
  data.append('first_name', first_name)
  data.append('last_name', last_name)
  data.append('gender', gender)
  data.append('birth', birth)
  preferred_categories.forEach(cat => data.append('preferred_categories', cat))
  preferred_books.forEach(book => data.append('preferred_books', book))
  if (profile_image) {
    data.append('profile_image', profile_image)
  }

  try {
    await store.signUp(data)
    await store.logIn({ username, password: password1 })
    alert('회원가입 및 로그인 완료!')
    router.push('/')
  } catch (err) {
    alert('회원가입 실패! 다시 시도해 주세요.')
  }
}

const nextStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}
</script>

<style scoped>
.panel {
  width: 580px;
  height: 500px inherit;
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

h1.animate1 {
  padding-top: 30px;
  padding-bottom: 60px;
  font-size: 24px;
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

.progress-bar {
  display: flex;
  justify-content: center;
  flex-direction: row;
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