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

    const signUp = (payload) => {
      const isFormData = payload instanceof FormData;
      return axios({
        method: "POST",
        url: `${ACCOUNT_API}/signup/`,
        data: payload,
        headers: isFormData ? {} : { "Content-Type": "application/json" },
      })
        .then(() => router.push("/"))
        .catch((err) => {
          console.error("회원가입 실패:", err.response?.data || err.message);
          throw err;
        });
    };

    const logIn = (credentials) =>
      axios
        .post(`${ACCOUNT_API}/login/`, credentials)
        .then((res) => {
          token.value = res.data.key;
          router.push("/");
        })
        .catch((err) =>
          console.error("로그인 실패:", err.response?.data || err.message)
        );

    const logOut = () =>
      axios
        .post(`${ACCOUNT_API}/logout/`, null, {
          headers: { Authorization: `Token ${token.value}` },
        })
        .then(() => {
          token.value = "";
          router.push("/login");
        })
        .catch((err) =>
          console.error("로그아웃 실패:", err.response?.data || err.message)
        );

    const fetchUserProfile = () => {
      return axios
        .get(`${ACCOUNT_API}/profile/`, {
          headers: { Authorization: `Token ${token.value}` },
        })
        .then((res) => {
          user.value = res.data;
        })
        .catch((err) => {
          console.error(
            "사용자 정보 불러오기 실패:",
            err.response?.data || err.message
          );
        });
    };

    return {
      signUp,
      logIn,
      logOut,
      token,
      isLogIn,
      fetchUserProfile,
      user
    };
  },
  { persist: true }
);
