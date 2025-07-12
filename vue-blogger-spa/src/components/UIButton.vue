<template>
  <button
    :class="[
      'ui-button',
      `ui-button--${variant}`,
      `ui-button--${size}`,
      { 'ui-button--loading': loading }
    ]"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
    v-bind="$attrs"
  >
    <span v-if="loading" class="ui-button__loader"></span>
    <span class="ui-button__content" :class="{ 'ui-button__content--hidden': loading }">
      <slot></slot>
    </span>
    <UITooltip v-if="tooltip" :text="tooltip">
      <span class="ui-button__tooltip-trigger"></span>
    </UITooltip>
  </button>
</template>

<script setup lang="ts">
import UITooltip from './UITooltip.vue';

defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'secondary', 'outline', 'text', 'danger', 'success'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value: string) => ['small', 'medium', 'large'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  tooltip: {
    type: String,
    default: ''
  }
});

defineEmits(['click']);
</script>

<style scoped>
.ui-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  font-family: var(--font-family);
  font-weight: var(--font-weight-medium);
  border-radius: var(--border-radius);
  border: none;
  cursor: pointer;
  transition: all var(--transition-speed) var(--transition-timing);
  white-space: nowrap;
  overflow: hidden;
}

/* Size variants */
.ui-button--small {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-sm);
  height: 30px;
}

.ui-button--medium {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-md);
  height: 38px;
}

.ui-button--large {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: var(--font-size-md);
  height: 46px;
}

/* Color variants */
.ui-button--primary {
  background-color: var(--primary-color);
  color: white;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
}

.ui-button--primary:hover,
.ui-button--primary:focus {
  background-color: var(--primary-dark);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
  transform: translateY(-1px);
}

.ui-button--primary:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(52, 152, 219, 0.2);
}

.ui-button--secondary {
  background-color: #f5f5f5;
  color: var(--text-color);
}

.ui-button--secondary:hover,
.ui-button--secondary:focus {
  background-color: #e9e9e9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ui-button--outline {
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.ui-button--outline:hover,
.ui-button--outline:focus {
  background-color: rgba(52, 152, 219, 0.05);
}

.ui-button--text {
  background-color: transparent;
  color: var(--primary-color);
  padding-left: var(--spacing-xs);
  padding-right: var(--spacing-xs);
}

.ui-button--text:hover,
.ui-button--text:focus {
  background-color: rgba(52, 152, 219, 0.05);
}

.ui-button--danger {
  background-color: var(--error-color);
  color: white;
}

.ui-button--danger:hover,
.ui-button--danger:focus {
  background-color: #c0392b;
  box-shadow: 0 2px 4px rgba(231, 76, 60, 0.2);
}

.ui-button--success {
  background-color: var(--success-color);
  color: white;
}

.ui-button--success:hover,
.ui-button--success:focus {
  background-color: #27ae60;
  box-shadow: 0 2px 4px rgba(46, 204, 113, 0.2);
}

/* States */
.ui-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

/* Loading state */
.ui-button--loading {
  cursor: wait;
}

.ui-button__content--hidden {
  opacity: 0;
}

.ui-button__loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Tooltip trigger (invisible element) */
.ui-button__tooltip-trigger {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Focus */
.ui-button:focus {
  outline: none;
}

.ui-button:focus-visible {
  box-shadow: 0 0 0 2px var(--primary-color);
}
</style>
