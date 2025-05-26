<template>
  <div class="container py-4" v-if="quizzes.length">
    <h2 class="mb-3">📚 퀴즈 도전</h2>
    <form @submit.prevent="submitQuiz">
      <div v-for="(quiz, index) in quizzes" :key="quiz.id" class="mb-4">
        <h5>{{ index + 1 }}. {{ quiz.question }}</h5>
        <div v-for="(text, key) in quiz.choices" :key="key" class="form-check">
          <input
            class="form-check-input"
            type="radio"
            :name="'quiz-' + index"
            :value="key"
            v-model="answers[index]"
            :id="`q${index}-${key}`"
          />
          <label class="form-check-label" :for="`q${index}-${key}`">
            {{ key }}. {{ text }}
          </label>
        </div>
      </div>
      <button class="btn btn-primary mt-3">제출</button>
    </form>
  </div>

  <div v-else-if="error" class="alert alert-warning mt-4 text-center">{{ error }}</div>
  <div v-else class="text-center mt-4">⏳ 퀴즈를 불러오는 중입니다...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter()
const store = useAccountStore()

const challengeId = route.params.challengeId
const quizzes = ref([])
const answers = ref([])
const error = ref(null)

const fetchQuizzes = async () => {
  try {
    const { data } = await axios.get(`http://127.0.0.1:8000/api/v1/quiz/start?challenge=${challengeId}`, {
      headers: { Authorization: `Token ${store.token}` },
    })
    quizzes.value = data
    answers.value = Array(data.length).fill(null)
    console.log("퀴즈 응답:", data)
    console.log("토큰 확인:", store.token)
  } catch (err) {
    console.error('퀴즈 로드 실패:', err)
    error.value = err.response?.data?.error || '퀴즈를 불러오지 못했습니다.'
  }
}

const submitQuiz = async () => {
  const correct = quizzes.value.filter((q, i) => q.answer === answers.value[i])
  const score = correct.length * 10

  try {
    await axios.post(
      'http://127.0.0.1:8000/api/v1/quiz/submit/',
      { challenge: challengeId, score },
      { headers: { Authorization: `Token ${store.token}` } }
    )
    alert(`✅ 당신의 점수는 ${score}점입니다!`)
    router.push(`/challenges/${challengeId}`)
  } catch (err) {
    console.error('퀴즈 제출 실패:', err)
    alert('퀴즈 제출 중 오류가 발생했습니다.')
  }
}

onMounted(fetchQuizzes)
</script>

<style scoped>
h5 {
  font-weight: 600;
}
</style>
