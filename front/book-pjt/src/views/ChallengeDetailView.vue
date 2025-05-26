<template>
  <div class="challenge-detail">
    <h2>{{ challenge?.title }}</h2>
    <p>{{ challenge?.description }}</p>
    <p>🔕️ {{ challenge?.start_date }} ~ {{ challenge?.end_date }}</p>
    <p>🎯 목표 도서 수: {{ challenge?.target_books }}</p>
    <p>👤 생성자: {{ challenge?.creator_username }}</p>

    <div class="my-3">
      <button
        class="btn"
        :class="isParticipant ? 'btn-danger' : 'btn-primary'"
        @click="isParticipant ? leaveChallenge() : joinChallenge()"
        :disabled="isCreator"
      >
        {{
          isCreator
            ? "생성자는 참여 취소 불가"
            : isParticipant
            ? "참여 취소하기"
            : "참여하기"
        }}
      </button>
    </div>
    <button
      v-if="isParticipant && challenge?.is_completed"
      class="btn btn-success my-2"
      disabled
    >
      🎉 퀴즈 성공
    </button>

    <!-- ✅ 참여자는 도전 가능 -->
    <RouterLink
      v-else-if="isParticipant"
      :to="{ name: 'QuizView', params: { challengeId: challenge.id } }"
      class="btn btn-outline-success my-2"
    >
      📘 퀴즈 도전하기
    </RouterLink>

    <!-- ✅ 미참여자 -->
    <p v-else class="text-muted">챌린지에 참여해야 퀴즈 도전이 가능합니다.</p>
    <!-- 참여자 목록 -->
    <div class="mt-4">
      <h4>참여자 목록</h4>
      <ul v-if="participants.length">
        <li v-for="user in participants" :key="user.id">
          {{ user.username }}
        </li>
      </ul>
      <p v-else>참여한 사용자가 없습니다.</p>
    </div>

    <!-- 댓글 -->
    <div class="mt-4">
      <h4>댓글</h4>
      <ul v-if="comments.length">
        <li v-for="comment in comments" :key="comment.id" class="mb-2">
          <strong>{{ comment.username }}</strong> -
          {{ comment.created_at.slice(0, 10) }}<br />
          <span>{{ comment.content }}</span>
          <div v-if="comment.username === store.user?.username">
            <button @click="editComment(comment)">수정</button>
            <button @click="deleteComment(comment.id)">삭제</button>
          </div>
        </li>
      </ul>
      <div class="mt-3">
        <textarea
          v-model="newComment"
          rows="2"
          class="form-control"
          placeholder="댓글을 입력하세요"
        ></textarea>
        <button class="btn btn-secondary mt-2" @click="submitComment">
          작성
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accounts";

const route = useRoute();
const router = useRouter();
const store = useAccountStore();

const challenge = ref(null);
const participants = ref([]);
const comments = ref([]);
const newComment = ref("");
const challengeId = route.params.id;

const isParticipant = ref(false);
const isCreator = computed(
  () => store.user?.username === challenge.value?.creator_username
);

const fetchChallenge = async () => {
  try {
    const { data } = await axios.get(
      `http://127.0.0.1:8000/api/v1/challenges/${challengeId}/`,
      { headers: { Authorization: `Token ${store.token}` } } 
    );
    challenge.value = data;
  } catch (err) {
    console.error("챌린지 정보 로드 실패:", err.response?.data || err);
  }
};

const fetchParticipants = async () => {
  try {
    const { data } = await axios.get(
      `http://127.0.0.1:8000/api/v1/participants/?challenge=${challengeId}`
    );
    participants.value = data;
    isParticipant.value = data.some((p) => p.username === store.user?.username);
  } catch (err) {
    console.error("참여자 정보 로드 실패:", err.response?.data || err);
  }
};

const fetchComments = async () => {
  try {
    const { data } = await axios.get(
      `http://127.0.0.1:8000/api/v1/comments/?challenge=${challengeId}`
    );
    comments.value = data;
  } catch (err) {
    console.error("댓글 로딩 실패:", err);
  }
};

const joinChallenge = async () => {
  const token = store.token;
  try {
    await axios.post(
      "http://127.0.0.1:8000/api/v1/participants/",
      { challenge: challengeId },
      { headers: { Authorization: `Token ${token}` } }
    );
    alert("참여가 완료되었습니다.");
    fetchParticipants();
  } catch (err) {
    console.error("참여 실패:", err.response?.data || err);
    alert("참여 중 오류가 발생했습니다.");
  }
};

const leaveChallenge = async () => {
  const token = store.token;
  try {
    const myParticipant = participants.value.find(
      (p) => p.username === store.user?.username
    );
    if (!myParticipant) return alert("참여 정보를 찾을 수 없습니다.");

    await axios.delete(
      `http://127.0.0.1:8000/api/v1/participants/${myParticipant.id}/`,
      { headers: { Authorization: `Token ${token}` } }
    );
    alert("참여가 취소되었습니다.");
    fetchParticipants();
  } catch (err) {
    console.error("참여 취소 실패:", err);
    alert("참여 취소 중 오류가 발생했습니다.");
  }
};

const submitComment = async () => {
  const token = store.token;
  if (!newComment.value.trim()) return alert("댓글을 입력하세요");
  try {
    await axios.post(
      "http://127.0.0.1:8000/api/v1/comments/",
      { challenge: challengeId, content: newComment.value },
      { headers: { Authorization: `Token ${token}` } }
    );
    newComment.value = "";
    fetchComments();
  } catch (err) {
    console.error("댓글 작성 실패:", err);
  }
};

const editComment = async (comment) => {
  const content = prompt("댓글 수정", comment.content);
  if (content && content !== comment.content) {
    try {
      await axios.put(
        `http://127.0.0.1:8000/api/v1/comments/${comment.id}/`,
        { challenge: challengeId, content },
        { headers: { Authorization: `Token ${store.token}` } }
      );
      fetchComments();
    } catch (err) {
      console.error("댓글 수정 실패:", err);
    }
  }
};

const deleteComment = async (commentId) => {
  if (!confirm("정말 삭제하시겠습니까?")) return;
  try {
    await axios.delete(`http://127.0.0.1:8000/api/v1/comments/${commentId}/`, {
      headers: { Authorization: `Token ${store.token}` },
    });
    fetchComments();
  } catch (err) {
    console.error("댓글 삭제 실패:", err);
  }
};

onMounted(() => {
  fetchChallenge();
  fetchParticipants();
  fetchComments();
});

watch(() => route.params.id, () => {
  fetchChallenge();
  fetchParticipants();
  fetchComments();
});
</script>


<style scoped>
.challenge-detail {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
