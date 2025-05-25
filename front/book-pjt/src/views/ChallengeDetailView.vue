<template>
  <div class="container py-4" v-if="challenge">
    <h2 class="mb-3">{{ challenge.title }}</h2>
    <p class="text-muted">작성자: {{ challenge.creator_username }}</p>
    <p>{{ challenge.description }}</p>
    <p class="text-secondary">
      기간: {{ challenge.start_date }} ~ {{ challenge.end_date }} / 목표: {{ challenge.target_books }}권
    </p>

    <!-- 참여 버튼 -->
    <div class="mb-4">
      <button @click="joinChallenge" class="btn btn-success" v-if="!isJoined">
        ✅ 참여하기
      </button>
      <span v-else class="text-success fw-bold">이미 참여 중입니다.</span>
    </div>

    <!-- 댓글 섹션 -->
    <div class="border-top pt-4">
      <h4>💬 댓글</h4>
      <form @submit.prevent="submitComment" class="mb-3">
        <textarea v-model="newComment" class="form-control" placeholder="댓글을 입력하세요" rows="2" required></textarea>
        <button class="btn btn-primary mt-2">댓글 작성</button>
      </form>

      <div v-if="comments.length">
        <div v-for="comment in comments" :key="comment.id" class="mb-2 p-2 bg-light rounded">
          <strong>{{ comment.username }}</strong> - {{ comment.created_at.slice(0, 10) }}
          <p class="mb-0">{{ comment.content }}</p>
        </div>
      </div>
      <p v-else>댓글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const store = useAccountStore()
const route = useRoute()
const API_URL = 'http://127.0.0.1:8000/api/v1'

const challenge = ref(null)
const comments = ref([])
const newComment = ref('')
const isJoined = ref(false)

const fetchChallenge = () => {
  axios.get(`${API_URL}/challenges/${route.params.id}/`)
    .then(res => {
      challenge.value = res.data
    })
}

const fetchComments = () => {
  axios.get(`${API_URL}/comments/?challenge=${route.params.id}`)
    .then(res => {
      comments.value = res.data.filter(c => c.challenge === parseInt(route.params.id))
    })
}

const checkJoined = () => {
  axios.get(`${API_URL}/participants/`, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(res => {
      isJoined.value = res.data.some(p => p.challenge === parseInt(route.params.id) && p.user === store.user.id)
    })
}

const joinChallenge = () => {
  axios.post(`${API_URL}/participants/`, {
    challenge: route.params.id,
  }, {
    headers: { Authorization: `Token ${store.token}` }
  }).then(() => {
    isJoined.value = true
  }).catch(err => console.error(err))
}

const submitComment = () => {
  axios.post(`${API_URL}/comments/`, {
    challenge: route.params.id,
    content: newComment.value,
  }, {
    headers: { Authorization: `Token ${store.token}` }
  }).then(() => {
    newComment.value = ''
    fetchComments()
  }).catch(err => console.error(err))
}

onMounted(() => {
  fetchChallenge()
  fetchComments()
  checkJoined()
})
</script>
