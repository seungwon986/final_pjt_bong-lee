// src/stores/challenge.js
import { defineStore } from 'pinia'


export const useChallengeStore = defineStore('challenge', {
  state: () => ({
    categories: [],
    challenges: [],
    activeCategory: 'All',
    loading: false,
    error: null,
  }),
  actions: {
    async loadCategories() {
      try {
        this.categories = ['All', ...(await fetchCategories())]
        this.activeCategory = 'All'
      } catch {
        this.error = '카테고리 로드 실패'
      }
    },
    async loadChallenges() {
      this.loading = true
      this.error = null
      try {
        const cat = this.activeCategory === 'All' ? undefined : this.activeCategory
        this.challenges = await fetchChallenges(cat)
      } catch {
        this.error = '챌린지 로드 실패'
      } finally {
        this.loading = false
      }
    },
    selectCategory(cat) {
      this.activeCategory = cat
      this.loadChallenges()
    }
  },
  getters: {
    filteredChallenges(state) {
      return state.activeCategory === 'All'
        ? state.challenges
        : state.challenges.filter(c => c.category === state.activeCategory)
    }
  }
})
