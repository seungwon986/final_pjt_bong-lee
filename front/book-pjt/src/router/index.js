import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

import Main from '@/views/Main.vue'
import BooksListView from '@/views/BooksListView.vue'
import SignUpView from '@/views/SignUpView.vue'
import MyPageView from '@/views/MyPageView.vue'
import LogInView from '@/views/LogInView.vue'
import ChallengeListView from '@/views/ChallengeListView.vue'
import CommunityView from '@/views/CommunityView.vue'

const routes = [
  { path: '/', name: 'main', component: Main },
  { path: '/books', name: 'books', component: BooksListView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/login', name: 'login', component: LogInView },
  { path: '/mypage', name: 'MyPage', component: MyPageView, meta: { requiresAuth: true } },
  { path: '/challenge/list', name: 'challenge-list', component: ChallengeListView },
  { path: '/community', name: 'community', component: CommunityView },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// 🔐 전역 가드 추가
router.beforeEach((to, from, next) => {
  const store = useAccountStore()
  if (to.meta.requiresAuth && !store.isLogIn) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
