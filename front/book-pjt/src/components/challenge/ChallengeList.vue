
<template>
  <div>
    <ChallengeCard
      v-for="challenge in challenges"
      :key="challenge.id"
      :challenge="challenge"
    />
  </div>
</template>

<script setup>
import ChallengeCard from './ChallengeCard.vue'

defineProps({
  challenges: Array
})
</script>
