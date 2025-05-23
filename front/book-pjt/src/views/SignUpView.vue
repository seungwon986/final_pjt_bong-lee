<template>
  <div class="container py-4">
    <div class="card p-4 shadow">
      <h2 class="mb-4">회원가입</h2>

      <component
        :is="steps[currentStep]"
        :form="form"
        @next="nextStep"
        @prev="prevStep"
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


const form = ref({
  username: '',
  password1: '',
  nickname: '',
  gender: '',
  birth: '',
  preferred_categories: [],
  preferred_books: [],
})


const currentStep = ref(0)
const steps = [SignUpStep1, SignUpStep2, SignUpStep3, SignUpStep4]

const nextStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}
</script>

<style scoped>
.container {
  max-width: 700px;
}
</style>
