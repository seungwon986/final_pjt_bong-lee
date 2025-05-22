<template>
  <form @submit.prevent="$emit('next')">
    <div class="mb-3">
      <label class="form-label">아이디</label>
      <input type="text" class="form-control" v-model="form.username" required />
    </div>
    
    <div class="mb-3">
      <label class="form-label">비밀번호</label>
      <input type="password" class="form-control" v-model="form.password1" required />
    </div>

    <div class="mb-3">
      <label class="form-label">비밀번호 확인</label>
      <input type="password" class="form-control" v-model="form.password2" required />
    </div>

    <div class="mb-3">
      <label class="form-label">닉네임</label>
      <input type="text" class="form-control" v-model="form.nickname" required />
    </div>

    <!-- ✅ 추가: 이름 -->
    <div class="mb-3">
      <label class="form-label">이름</label>
      <input type="text" class="form-control" v-model="form.first_name" required />
    </div>

    <!-- ✅ 추가: 성 -->
    <div class="mb-3">
      <label class="form-label">성</label>
      <input type="text" class="form-control" v-model="form.last_name" required />
    </div>

    <div class="mb-3">
      <label class="form-label">생년월일</label>
      <input type="date" class="form-control" v-model="form.birth" required />
    </div>

    <div class="mb-3">
      <label class="form-label">성별</label>
      <select class="form-select" v-model="form.gender" required>
        <option value="M">남성</option>
        <option value="F">여성</option>
      </select>
    </div>

    <div class="mb-3">
      <label class="form-label">프로필 이미지</label>
      <input type="file" class="form-control" @change="onFileChange" />
    </div>

    <button type="submit" class="btn btn-primary">다음</button>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:user', 'next'])

const form = reactive({ ...props.modelValue })

watch(form, () => emit('update:user', form), { deep: true })

const onFileChange = (e) => {
  form.profile_image = e.target.files[0]
}
</script>
