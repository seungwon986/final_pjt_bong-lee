import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'
import BooksListView from '@/views/BooksListView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ChallengeListView from '@/views/ChallengeListView.vue'  
import CommunityView from '@/views/CommunityView.vue'
import ChallengeCreateView from '@/views/ChallengeCreateView.vue'
const routes = [
  { path: '/',       name: 'main',   component: Main },
  { path: '/books',  name: 'books',  component: BooksListView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/login',  name: 'login',  component: LogInView },
  // { path: '/challenge/list',name: 'ChallengeList',component: ChallengeListView},
  // { path: '/community', name: 'Community', component: CommunityView },
  // { path: '/challenge/create', name: 'ChallengeCreate', component: ChallengeCreateView}
]


export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})
