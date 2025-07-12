<template>
  <div class="tooltip-wrapper">
    <div ref="triggerRef" @mouseenter="showTooltip" @mouseleave="hideTooltip" @focus="showTooltip" @blur="hideTooltip">
      <slot></slot>
    </div>
    <Teleport to="body">
      <transition name="tooltip">
        <div
          v-if="isVisible"
          ref="tooltipRef"
          class="tooltip"
          :class="[position]"
          :style="tooltipStyle"
          role="tooltip"
        >
          {{ text }}
          <div class="tooltip-arrow"></div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onUnmounted } from 'vue';

const props = defineProps({
  text: {
    type: String,
    required: true
  },
  position: {
    type: String,
    default: 'top',
    validator: (value: string) => ['top', 'bottom', 'left', 'right'].includes(value)
  },
  delay: {
    type: Number,
    default: 200
  }
});

const isVisible = ref(false);
const triggerRef = ref<HTMLElement | null>(null);
const tooltipRef = ref<HTMLElement | null>(null);
const tooltipStyle = ref({});
let showTimer: number | null = null;

function calculatePosition() {
  if (!triggerRef.value || !tooltipRef.value) return;

  const triggerRect = triggerRef.value.getBoundingClientRect();
  const tooltipRect = tooltipRef.value.getBoundingClientRect();

  let top = 0;
  let left = 0;

  switch (props.position) {
    case 'top':
      top = triggerRect.top - tooltipRect.height - 10;
      left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
      break;
    case 'bottom':
      top = triggerRect.bottom + 10;
      left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
      break;
    case 'left':
      top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
      left = triggerRect.left - tooltipRect.width - 10;
      break;
    case 'right':
      top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
      left = triggerRect.right + 10;
      break;
  }

  tooltipStyle.value = {
    top: `${top}px`,
    left: `${left}px`
  };
}

function showTooltip() {
  showTimer = window.setTimeout(() => {
    isVisible.value = true;
    nextTick(() => calculatePosition());
  }, props.delay);
}

function hideTooltip() {
  if (showTimer) {
    clearTimeout(showTimer);
    showTimer = null;
  }
  isVisible.value = false;
}

onUnmounted(() => {
  if (showTimer) {
    clearTimeout(showTimer);
  }
});
</script>

<style scoped>
.tooltip-wrapper {
  display: inline-block;
  position: relative;
}

.tooltip {
  position: fixed;
  z-index: 10000;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  font-size: var(--font-size-sm);
  max-width: 250px;
  text-align: center;
  pointer-events: none;
  box-shadow: var(--box-shadow);
}

.tooltip-arrow {
  position: absolute;
  width: 0;
  height: 0;
  border: 5px solid transparent;
}

.tooltip.top .tooltip-arrow {
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-top-color: rgba(0, 0, 0, 0.8);
}

.tooltip.bottom .tooltip-arrow {
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-bottom-color: rgba(0, 0, 0, 0.8);
}

.tooltip.left .tooltip-arrow {
  right: -10px;
  top: 50%;
  transform: translateY(-50%);
  border-left-color: rgba(0, 0, 0, 0.8);
}

.tooltip.right .tooltip-arrow {
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  border-right-color: rgba(0, 0, 0, 0.8);
}

/* Tooltip transition */
.tooltip-enter-active,
.tooltip-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
