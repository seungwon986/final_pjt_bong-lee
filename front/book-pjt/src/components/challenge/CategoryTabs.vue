<!-- src/components/challenge/CategoryTabs.vue -->
<template>
  <div class="category-tabs">
    <button
      v-for="cat in categories"
      :key="cat"
      :class="['tab', { active: cat === active }]"
      @click="$emit('select', cat)"
    >
      {{ cat }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  categories: Array,
  active: String,
})
defineEmits(['select'])
</script>

<style scoped>
.category-tabs {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  margin-bottom: 1rem;
}
.tab {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #eee;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
}
.tab.active {
  background-color: #007bff;
  color: white;
}
</style>
