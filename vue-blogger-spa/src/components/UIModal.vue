<template>
  <Teleport to="body">
    <transition name="modal-fade">
      <div v-if="modelValue" class="modal-overlay" @click="closeOnOverlayClick && $emit('update:modelValue', false)">
        <div
          class="modal-container"
          :class="{
            [`modal-size-${size}`]: true,
            'modal-scrollable': scrollable
          }"
          @click.stop
          role="dialog"
          aria-modal="true"
          :aria-labelledby="titleId"
        >
          <div class="modal-header">
            <h3 :id="titleId" class="modal-title">
              <slot name="title">{{ title }}</slot>
            </h3>
            <button
              v-if="showCloseButton"
              class="modal-close-button"
              @click="$emit('update:modelValue', false)"
              aria-label="Close modal"
            >
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <div class="modal-body" :class="{ 'has-footer': $slots.footer }">
            <slot></slot>
          </div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value: string) => ['small', 'medium', 'large', 'full'].includes(value)
  },
  scrollable: {
    type: Boolean,
    default: false
  },
  closeOnOverlayClick: {
    type: Boolean,
    default: true
  },
  showCloseButton: {
    type: Boolean,
    default: true
  }
});

const titleId = ref(`modal-title-${Math.random().toString(36).substr(2, 9)}`);

const emit = defineEmits(['update:modelValue']);

// Handle ESC key to close the modal
function handleKeyDown(event: KeyboardEvent) {
  if (event.key === 'Escape' && props.modelValue) {
    event.preventDefault();
    event.stopPropagation();
    emit('update:modelValue', false);
  }
}

// Prevent body scrolling when modal is open
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}, { immediate: true });

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  document.body.style.overflow = '';
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
}

.modal-container {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - var(--spacing-xl) * 2);
  width: 100%;
}

.modal-size-small {
  max-width: 400px;
}

.modal-size-medium {
  max-width: 600px;
}

.modal-size-large {
  max-width: 800px;
}

.modal-size-full {
  max-width: 100%;
  height: 100%;
  max-height: 100vh;
  border-radius: 0;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.modal-title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--text-color);
}

.modal-close-button {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: var(--text-secondary);
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: var(--border-radius);
  transition: all var(--transition-speed) var(--transition-timing);
}

.modal-close-button:hover,
.modal-close-button:focus {
  color: var(--text-color);
  background-color: rgba(0, 0, 0, 0.05);
}

.modal-body {
  padding: var(--spacing-lg);
  overflow-y: auto;
  flex: 1;
}

.modal-body.has-footer {
  border-bottom: 1px solid var(--border-color);
}

.modal-scrollable .modal-body {
  max-height: 50vh;
  overflow-y: auto;
}

.modal-footer {
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--spacing-sm);
}

/* Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from {
  opacity: 0;
}

.modal-fade-enter-from .modal-container {
  transform: scale(0.9);
}

.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-leave-to .modal-container {
  transform: scale(0.9);
}

@media (max-width: 768px) {
  .modal-size-small,
  .modal-size-medium,
  .modal-size-large {
    max-width: 100%;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding: var(--spacing-md);
  }
}
</style>
