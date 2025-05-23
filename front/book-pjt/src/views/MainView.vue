<template>
  <div class="main-container">
    <HeroSection />
    <CategoryButtons />
    <BestSeller />
    <CelebrityPicks />
  </div>
</template>

<script setup>
import HeroSection from '@/components/main/HeroSection.vue'
import CategoryButtons from '@/components/main/CategoryButtons.vue'
import BestSellerCarousel from '@/components/main/BestSeller.vue'
</script>

<style scoped>
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
}
</style>
