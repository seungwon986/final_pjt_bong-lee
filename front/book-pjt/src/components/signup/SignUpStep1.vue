<template>
  <div>
    <h3>기본 정보를 입력하세요</h3>
    <form @submit.prevent="handleNext" enctype="multipart/form-data">
      <div class="mb-3">
        <label class="form-label">아이디</label>
        <input type="text" class="form-control" v-model="form.username" required>
      </div>

      <div class="mb-3">
        <label class="form-label">비밀번호</label>
        <input type="password" class="form-control" v-model="form.password1" required>
      </div>

      <div class="mb-3">
        <label class="form-label">비밀번호 확인</label>
        <input type="password" class="form-control" v-model="form.password2" required>
      </div>

      <div class="mb-3">
        <label class="form-label">닉네임</label>
        <input type="text" class="form-control" v-model="form.nickname" required>
      </div>

      <div class="mb-3">
        <label class="form-label">이름</label>
        <input type="text" class="form-control" v-model="form.first_name" required>
      </div>

      <div class="mb-3">
        <label class="form-label">성</label>
        <input type="text" class="form-control" v-model="form.last_name" required>
      </div>

      <div class="mb-3">
        <label class="form-label">성별</label>
        <select class="form-select" v-model="form.gender" required>
          <option disabled value="">선택하세요</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">생년월일</label>
        <input type="date" class="form-control" v-model="form.birth" required>
      </div>

      <div class="mb-3">
        <label class="form-label">프로필 이미지</label>
        <input type="file" class="form-control" @change="onFileChange" accept="image/*">
      </div>

      <div class="mt-4 d-flex justify-content-end">
        <button type="submit" class="btn btn-primary">다음</button>
      </div>
    </form>
  </div>
</template>

<script setup>
const props = defineProps({
  form: Object
})

const emit = defineEmits(['next'])

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    props.form.profile_image = file
  }
}

const handleNext = () => {
  const {
    username, password1, password2, nickname,
    first_name, last_name, gender, birth
  } = props.form

  if (!username || !password1 || !password2 || !nickname || !first_name || !last_name || !gender || !birth) {
    alert('모든 항목을 입력해주세요.')
    return
  }

  if (password1.length < 8 || !/\d/.test(password1) || !/[a-zA-Z]/.test(password1)) {
    alert('비밀번호는 8자 이상, 문자와 숫자를 포함해야 합니다.')
    return
  }

  if (password1 !== password2) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  emit('next')
}
</script>

<style scoped>
</style>
