<template>
  <div
    v-if="isLoading"
    class="loading-indicator"
    :style="{
      transform: `scaleX(${progress / 100})`,
      transition: `transform ${transitionSpeed}ms ease-out`
    }"
    role="progressbar"
    aria-valuemin="0"
    aria-valuemax="100"
    :aria-valuenow="progress"
  ></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  },
  duration: {
    type: Number,
    default: 1000
  }
});

const progress = ref(0);
const transitionSpeed = ref(200);
let interval: number | null = null;

watch(() => props.isLoading, (newVal) => {
  if (newVal) {
    startProgress();
  } else {
    completeProgress();
  }
}, { immediate: true });

function startProgress() {
  progress.value = 0;

  if (interval) {
    clearInterval(interval);
  }

  // Start with a faster increase, then slow down as we approach 90%
  interval = window.setInterval(() => {
    if (progress.value < 90) {
      const increment = progress.value < 30 ? 10 :
                        progress.value < 60 ? 5 : 2;
      progress.value = Math.min(90, progress.value + increment);
    }
  }, props.duration / 10);
}

function completeProgress() {
  if (interval) {
    clearInterval(interval);
    interval = null;
  }

  // Jump to 100% and then hide
  progress.value = 100;
}

onMounted(() => {
  if (props.isLoading) {
    startProgress();
  }
});
</script>

<style scoped>
.loading-indicator {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, var(--primary-color), var(--accent-color));
  z-index: 9999;
  transform-origin: left;
}
</style>
