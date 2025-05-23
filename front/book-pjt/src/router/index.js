import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'
import BooksListView from '@/views/BooksListView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MyPageView from '@/views/MyPageView.vue'
const routes = [
  { path: '/',      name: 'main',       component: Main },
  { path: '/books', name: 'books',      component: BooksListView },
  { path: '/signup',name: 'SignUpView', component: SignUpView },
  { path: '/login', name: 'LogInView',  component: LogInView },
  { path: '/MyPage', name: 'MyPage', component: MyPageView },
]

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})
