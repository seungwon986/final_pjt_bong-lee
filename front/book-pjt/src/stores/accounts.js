import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

export const useAccountStore = defineStore(
  "account",
  () => {
    const ACCOUNT_API = "http://127.0.0.1:8000/accounts";
    const token = ref("");
    const user = ref(null);
    const router = useRouter();

    const isLogIn = computed(() => !!token.value);

    const signUp = async (payload) => {
      const isFormData = payload instanceof FormData;
      try {
        await axios({
          method: "POST",
          url: `${ACCOUNT_API}/signup/`,
          data: payload,
          headers: isFormData ? {} : { "Content-Type": "application/json" },
        });
      } catch (err) {
        console.error("회원가입 실패:", err.response?.data || err.message);
        throw err;
      }
    };

    const logIn = async (credentials) => {
      try {
        const res = await axios.post(`${ACCOUNT_API}/login/`, credentials);
        token.value = res.data.key;

        // ✅ 사용자 정보 요청
        await fetchUserProfile();

        // ✅ 메인 페이지로 이동
        router.push("/");
      } catch (err) {
        console.error("로그인 실패:", err.response?.data || err.message);
        throw err;
      }
    };

    const logOut = async () => {
      try {
        await axios.post(`${ACCOUNT_API}/logout/`, null, {
          headers: { Authorization: `Token ${token.value}` },
        });
        token.value = "";
        user.value = null;
        router.push("/login");
      } catch (err) {
        console.error("로그아웃 실패:", err.response?.data || err.message);
      }
    };

    const fetchUserProfile = async () => {
      if (!token.value) return;
      try {
        const res = await axios.get(`${ACCOUNT_API}/profile/`, {
          headers: { Authorization: `Token ${token.value}` },
        });
        user.value = res.data;
      } catch (err) {
        console.error(
          "사용자 정보 불러오기 실패:",
          err.response?.data || err.message
        );
      }
    };

    return {
      signUp,
      logIn,
      logOut,
      token,
      isLogIn,
      fetchUserProfile,
      user,
    };
  },
  { persist: true }
);
