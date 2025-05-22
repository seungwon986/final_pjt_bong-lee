<template>
  <div class="container mt-5">
    <h2 class="mb-4">회원가입</h2>
    <component
      :is="steps[currentStep]"
      v-model:user="user"
      v-model:selectedCategories="selectedCategories"
      v-model:selectedBooks="selectedBooks"
      @next="currentStep++"
      @prev="currentStep--"
    />
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
</script>
