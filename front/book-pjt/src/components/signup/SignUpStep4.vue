<template>
  <div>
    <p>입력한 정보를 확인하고 회원가입 버튼을 눌러주세요</p>
    <div class="mb-3">
      <strong>아이디:</strong> {{ user.username }}<br />
      <strong>닉네임:</strong> {{ user.nickname }}<br />
      <strong>성별:</strong> {{ user.gender === "M" ? "남성" : "여성" }}<br />
      <strong>생년월일:</strong> {{ user.birth }}
    </div>

    <div v-if="books.length">
      <h5>선택한 책</h5>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="book in books" :key="book.id" class="col">
          <div class="card h-100">
            <img :src="book.cover" class="card-img-top" alt="book cover" />
            <div class="card-body">
              <h5 class="card-title">{{ book.title }}</h5>
              <p class="card-text">{{ book.author }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-3">
      <button class="btn btn-secondary" @click="$emit('prev')">이전</button>
      <button class="btn btn-success" @click="submit">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useAccountStore } from "@/stores/accounts";

const props = defineProps(["user", "selectedBooks", "selectedCategories"]);
const books = ref([]);
const store = useAccountStore();

onMounted(() => {
  if (!props.selectedBooks.length) return;

  const query = props.selectedBooks.map((id) => `id=${id}`).join("&");
  axios
    .get(`http://127.0.0.1:8000/api/v1/books/?${query}`)
    .then((res) => {
      books.value = res.data;
    })
    .catch(() => alert("도서 정보를 불러오지 못했습니다."));
});

const submit = () => {
  const formData = new FormData();

  // 사용자 정보 추가
  for (const key in props.user) {
    formData.append(key, props.user[key]);
  }

  // 선택한 책 → preferred_books
  props.selectedBooks.forEach((bookId) =>
    formData.append("preferred_books", Number(bookId))
  );

  // 선택한 카테고리 → preferred_categories
  props.selectedCategories.forEach((catId) =>
    formData.append("preferred_categories", Number(catId))
  );

  store
    .signUp(formData)
    .then(() => alert("🎉 회원가입 성공!"))
    .catch(() => alert("회원가입에 실패했습니다."));
};
</script>
