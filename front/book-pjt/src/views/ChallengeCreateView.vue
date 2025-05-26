<template>
  <div class="challenge-create-wrapper">
    <h2>챌린지 생성</h2>
    <div class="form-group">
      <label for="title">챌린지 제목</label>
      <input
        id="title"
        type="text"
        v-model="form.title"
        placeholder="챌린지 이름을 입력하세요"
        required
      />
    </div>
    <form @submit.prevent="submitChallenge">
      <!-- 최대 참여 인원 -->
      <div class="form-group">
        <label for="maxParticipants">최대 참여 인원</label>
        <input
          id="maxParticipants"
          type="number"
          v-model.number="form.maxParticipants"
          min="1"
          required
        />
      </div>

      <!-- 도서 카테고리 선택 -->
      <div class="form-group">
        <label for="category">도서 카테고리</label>
        <select id="category" v-model="form.category" required>
          <option value="" disabled>카테고리 선택</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <div class="form-group" v-if="categoryBooks.length && !selectedBook">
        <label for="bookSearch">도서 검색</label>
        <input
          id="bookSearch"
          type="text"
          v-model="searchQuery"
          placeholder="책 제목을 입력하세요"
          autocomplete="off"
        />
        <ul v-if="filteredBooks.length && searchQuery" class="suggestions-list">
          <li
            v-for="book in filteredBooks"
            :key="book.id"
            @click="selectBook(book)"
          >
            {{ truncate(book.title, 50) }}
            <span class="author">- {{ book.author }}</span>
          </li>
        </ul>

        <select v-model="form.book" class="form-control mt-2">
          <option disabled value="">또는 도서를 선택하세요</option>
          <option v-for="book in categoryBooks" :key="book.id" :value="book.id">
            {{ truncate(book.title, 60) }} - {{ book.author }}
          </option>
        </select>
      </div>

      <div class="form-group selected-book-card" v-if="selectedBook">
        <label>선택 도서</label>
        <div class="selected-book">
          <img :src="selectedBook.cover" :alt="selectedBook.title" />
          <div class="info">
            <p class="title">{{ selectedBook.title }}</p>
            <p class="author">{{ selectedBook.author }}</p>
          </div>
          <button type="button" class="btn-cancel" @click="clearSelection">
            선택 취소
          </button>
        </div>
      </div>

      <!-- 소개글 -->
      <div class="form-group">
        <label for="description">소개글</label>
        <textarea
          id="description"
          v-model="form.description"
          rows="4"
          required
        ></textarea>
      </div>

      <!-- 시작일 & 마감일 -->
      <div class="form-group date-group">
        <div>
          <label for="startDate">시작일</label>
          <input id="startDate" type="date" v-model="form.startDate" required />
        </div>
        <div>
          <label for="endDate">마감일</label>
          <input id="endDate" type="date" v-model="form.endDate" required />
        </div>
      </div>

      <!-- 진행 기간 -->
      <div class="form-group">
        <label>진행 기간</label>
        <input type="text" :value="duration" readonly />
      </div>

      <!-- 제출 버튼 -->
      <button type="submit" class="btn-submit">챌린지 생성</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from "vue";
import axios from "axios";
import { useAccountStore } from "@/stores/accounts"; // Pinia store
import { useRouter } from "vue-router";

const router = useRouter();
const store = useAccountStore();

const categories = ref([]);
const categoryBooks = ref([]);
const searchQuery = ref("");

const form = reactive({
  title: "",
  description: "",
  startDate: "",
  endDate: "",
  target_books: 1,
  category: "",
  book: "",
});

const selectedBook = computed(() =>
  categoryBooks.value.find((book) => book.id === form.book)
);

const filteredBooks = computed(() =>
  searchQuery.value
    ? categoryBooks.value.filter((book) =>
        book.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    : categoryBooks.value
);

const truncate = (str, max = 50) =>
  str.length > max ? str.slice(0, max) + "..." : str;

const fetchCategories = async () => {
  try {
    const { data } = await axios.get(
      "http://127.0.0.1:8000/api/v1/books/categories/"
    );
    categories.value = data;
  } catch (e) {
    console.error("카테고리 불러오기 실패", e);
  }
};

watch(
  () => form.category,
  async (newVal) => {
    if (!newVal) return;
    try {
      const { data } = await axios.get(
        `http://127.0.0.1:8000/api/v1/books?category=${newVal}`
      );
      categoryBooks.value = data;
    } catch (e) {
      console.error("카테고리 도서 로드 실패", e);
    }
  }
);

function selectBook(book) {
  form.book = book.id;
  searchQuery.value = book.title;
}

function clearSelection() {
  form.book = null;
  searchQuery.value = "";
}

watch(
  () => form.book,
  (newVal) => {
    if (newVal && !selectedBook.value) {
      const book = categoryBooks.value.find((b) => b.id === newVal);
      if (book) searchQuery.value = book.title;
    }
  }
);

const duration = computed(() => {
  if (!form.startDate || !form.endDate) return "";
  const start = new Date(form.startDate);
  const end = new Date(form.endDate);
  const diff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
  return `${diff}일`;
});

watch(
  () => form.startDate,
  () => {
    if (form.endDate && form.endDate < form.startDate) {
      form.endDate = "";
    }
  }
);

const submitChallenge = async () => {
  const payload = {
    title: form.title,
    description: form.description,
    start_date: form.startDate,
    end_date: form.endDate,
    target_books: form.target_books,
    book: form.book, // foreign key id
  };

  try {
    const token = store.token || localStorage.getItem("token");
    const headers = token ? { Authorization: `Token ${token}` } : {};

    const { data } = await axios.post(
      "http://127.0.0.1:8000/api/v1/challenges/",
      payload,
      { headers }
    );
    alert("챌린지가 생성되었습니다!");
    router.push("/challenges");
  } catch (e) {
    console.error("챌린지 생성 실패:", e.response?.data || e);
    alert("생성 중 오류가 발생했습니다.");
  }
};

onMounted(fetchCategories);
</script>

<style scoped>
.challenge-create-wrapper {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}
.form-group label {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #34495e;
}
.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #dcdfe6;
  border-radius: 0.5rem;
}
.date-group {
  display: flex;
  gap: 1rem;
}
.suggestions-list {
  margin: 0.25rem 0 0;
  padding: 0;
  list-style: none;
  border: 1px solid #dcdfe6;
  border-radius: 0.5rem;
  max-height: 150px;
  overflow-y: auto;
  background: #fff;
}
.suggestions-list li {
  padding: 0.5rem;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.suggestions-list li .author {
  color: #888;
  font-size: 0.875rem;
}

.selected-book-card {
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.selected-book {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.selected-book img {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: 0.25rem;
}
.selected-book .info {
  flex: 1;
}
.selected-book .info .title {
  font-weight: bold;
}
.selected-book .info .author {
  color: #555;
  font-size: 0.875rem;
}
.btn-cancel {
  margin-left: auto;
  background: none;
  border: none;
  color: #dc3545;
  font-weight: bold;
  cursor: pointer;
}
.btn-cancel:hover {
  text-decoration: underline;
}
.btn-submit {
  width: 100%;
  padding: 0.75rem;
  background: #2c3e50;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
}
.btn-submit:hover {
  background: #1a252f;
}
</style>
