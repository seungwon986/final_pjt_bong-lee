import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

import Main from '@/views/Main.vue'
import BooksListView from '@/views/BooksListView.vue'
import SignUpView from '@/views/SignUpView.vue'
import MyPageView from '@/views/MyPageView.vue'
import LogInView from '@/views/LogInView.vue'
import ChallengeListView from '@/views/ChallengeListView.vue'
import ChallengeDetailView from '@/views/ChallengeDetailView.vue'
import CommunityView from '@/views/CommunityView.vue'
import ChallengeCreateView from '@/views/ChallengeCreateView.vue'

const routes = [
  { path: '/', name: 'main', component: Main },
  { path: '/books', name: 'books', component: BooksListView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/login', name: 'login', component: LogInView },
  { path: '/mypage', name: 'MyPage', component: MyPageView, meta: { requiresAuth: true } },
  { path: '/challenges', name: 'ChallengeList', component: ChallengeListView },
  { path: '/challenges/:id', name: 'ChallengeDetail', component: ChallengeDetailView, props: true },
  { path: '/community', name: 'community', component: CommunityView },
  {
  path: '/challenge/create',
  name: 'ChallengeCreate',
  component: ChallengeCreateView,
  meta: { requiresAuth: true },
}
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const store = useAccountStore()
  if (to.meta.requiresAuth && !store.isLogIn) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
