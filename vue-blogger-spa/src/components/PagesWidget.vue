<template>
  <div class="pages-widget">
    <h2 class="widget-title">Pages</h2>
    <div v-if="isLoading" class="loading" role="status" aria-live="polite">
      <div class="loading-spinner"></div>
      <p>Loading pages...</p>
    </div>
    <div v-else-if="error" class="error" role="alert">
      <p>{{ error }}</p>
      <button @click="pageStore.fetchPages" class="retry-button">
        <span class="retry-icon">↻</span> Try Again
      </button>
    </div>
    <ul v-else-if="pages.length > 0" class="pages-list">
      <li v-for="page in pages" :key="page.id" class="page-item">
        <router-link :to="page.url || `/page/${page.id}`" class="page-link">
          {{ page.title }}
        </router-link>
      </li>
    </ul>
    <p v-else class="no-pages">No pages available.</p>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { usePageStore } from '@/stores';

const pageStore = usePageStore();
const { pages, isLoading, error } = storeToRefs(pageStore);
</script>

<style scoped>
.pages-widget {
  background-color: white;
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
  box-shadow: var(--box-shadow);
  margin-bottom: var(--spacing-lg);
}

.widget-title {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
  color: var(--primary-color);
}

.pages-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.page-item {
  margin-bottom: var(--spacing-sm);
}

.page-link {
  display: block;
  color: var(--text-color);
  text-decoration: none;
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: background-color 0.2s, color 0.2s, transform 0.2s;
}

.page-link:hover {
  background-color: rgba(0, 0, 0, 0.03);
  color: var(--primary-color);
  transform: translateX(3px);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: var(--spacing-sm);
}

.error {
  color: var(--error-color);
  padding: var(--spacing-md);
  text-align: center;
}

.retry-button {
  margin-top: var(--spacing-sm);
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: var(--primary-dark);
}

.retry-icon {
  display: inline-block;
  margin-right: var(--spacing-xs);
}

.no-pages {
  color: var(--text-muted);
  text-align: center;
  padding: var(--spacing-md);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
