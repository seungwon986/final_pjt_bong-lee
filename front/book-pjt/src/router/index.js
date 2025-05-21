import { createRouter, createWebHistory } from 'vue-router'
import BooksListView from '@/views/BooksListView.vue'

const routes = [
  {
    path: '/books',
    name: 'books',
    component: BooksListView
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
