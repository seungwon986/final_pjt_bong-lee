<template>
  <div class="panel shadow1">
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

    <!-- 단계별 입력 화면 -->
    <div class="animate2 step-panel">
      <component
        :is="steps[currentStep]"
        :ref="currentStep === steps.length - 1 ? 'stepComponent' : null"
        :form="form"
        @next="nextStep"
        @prev="prevStep"
        @submit="submitForm"
      />
    </div>
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
const stepComponent = ref(null)

const store = useAccountStore()
const router = useRouter()

const submitForm = async () => {
  // Step4의 컴포넌트에서 expose한 isSubmitting 접근
  if (stepComponent.value?.isSubmitting) return
  stepComponent.value.isSubmitting = true

  const f = form.value

  const data = new FormData()
  data.append('username', f.username)
  data.append('password1', f.password1)
  data.append('password2', f.password2)
  data.append('nickname', f.nickname)
  data.append('first_name', f.first_name)
  data.append('last_name', f.last_name)
  data.append('gender', f.gender)
  data.append('birth', f.birth)
  if (f.profile_image) {
    data.append('profile_image', f.profile_image)
  }
  f.preferred_categories.forEach(cat => data.append('preferred_categories', cat))
  f.preferred_books.forEach(book => data.append('preferred_books', book))

  try {
    await store.signUp(data)
    await store.logIn({ username: f.username, password: f.password1 })
    alert('회원가입 및 로그인 완료!')
    router.push('/')
  } catch (err) {
    const msg =
      err?.response?.data?.nickname?.[0] ||
      err?.response?.data?.non_field_errors?.[0] ||
      err?.response?.data?.error ||
      "회원가입 중 오류가 발생했습니다."
    alert(msg)
  } finally {
    stepComponent.value.isSubmitting = false
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
  margin: 60px auto;
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
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
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
