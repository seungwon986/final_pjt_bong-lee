<template>
  <div>
    <p>기본 정보를 입력하세요</p>
    <form @submit.prevent="handleNext" enctype="multipart/form-data">


      <div class="mb-3">
        <label for="username" class="form-label">아이디</label>
        <input type="text" id="username" class="form-control" v-model="form.username" required>
      </div>

      <div class="mb-3">
        <label for="password1" class="form-label">비밀번호</label>
        <input type="password" id="password1" class="form-control" v-model="form.password1" required>
      </div>

      <div class="mb-3">
        <label for="password2" class="form-label">비밀번호 확인</label>
        <input type="password" id="password2" class="form-control" v-model="form.password2" required>
      </div>

      <div class="mb-3">
        <label for="nickname" class="form-label">닉네임</label>
        <input type="text" id="nickname" class="form-control" v-model="form.nickname" required>
      </div>

      <div class="mb-3">
        <label for="first-name" class="form-label">이름</label>
        <input type="text" id="first-name" class="form-control" v-model="form.first_name" required>
      </div>

      <div class="mb-3">
        <label for="last-name" class="form-label">성</label>
        <input type="text" id="last-name" class="form-control" v-model="form.last_name" required>
      </div>

      <div class="mb-3">
        <label for="gender" class="form-label">성별</label>
        <select  id="gender" class="form-select" v-model="form.gender" required>
          <option disabled value="">선택하세요</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="birth" class="form-label">생년월일</label>
        <input type="date" id="birth" class="form-control" v-model="form.birth" required>
      </div>

      <div class="mb-3">
        <label for="profile_image" class="form-label">프로필 이미지</label>
        <input type="file" id="profile_image" class="form-control" @change="onFileChange" accept="image/*">
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
    // Vue에서는 직접 props를 수정하는 방식이 불안정할 수 있으므로 아래처럼 안전하게 처리
    // 1) emit으로 처리
    emit('update-profile-image', file)

    // 2) 또는 setup에서 구조분해로 꺼내쓰기 (내부 속성만 수정하는 건 대개 안전함)
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
.signup-wrapper {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06);
}

.title {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 6px;
}

.subtitle {
  font-size: 14px;
  color: #888;
  text-align: center;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #444;
}

input,
select {
  width: 100%;
  padding: 12px 16px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 12px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus,
select:focus {
  border-color: #fc47b0;
}



p {
  text-align: center;
}

</style>
