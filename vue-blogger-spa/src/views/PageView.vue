<template>
  <div v-if="page" class="page-view">
    <div class="page-header">
      <h1>{{ page.title }}</h1>
      <div class="page-meta">
        <span class="page-date">Last updated: {{ formatDate(page.updated) }}</span>
      </div>
    </div>

    <div class="page-content" v-html="page.content"></div>

    <div class="page-navigation">
      <router-link to="/" class="back-link">
        &larr; Back to Home
      </router-link>
    </div>
  </div>
  <div v-else-if="isLoading" class="loading" role="status" aria-live="polite">
    <div class="loading-spinner"></div>
    <p>Loading page...</p>
  </div>
  <div v-else class="page-not-found">
    <h2>Page Not Found</h2>
    <p>The page you're looking for doesn't exist.</p>
    <router-link to="/" class="back-link">
      &larr; Back to Home
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { usePageStore } from '@/stores';

const route = useRoute();
const pageStore = usePageStore();

const pageId = computed(() => route.params.id as string);
const pageUrl = computed(() => route.path);

const page = computed(() => {
  if (route.params.id) {
    return pageStore.getPageById(pageId.value);
  } else if (route.path) {
    return pageStore.getPageByUrl(pageUrl.value);
  }
  return undefined;
});

const isLoading = computed(() => pageStore.isLoading);

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

onMounted(() => {
  // Force refresh pages data to ensure we have the latest content
  pageStore.fetchPages();
});
</script>

<style scoped>
.page-view {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-md);
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.page-header {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

h1 {
  color: var(--text-color);
  margin-bottom: var(--spacing-sm);
  font-size: 2rem;
  line-height: 1.3;
}

.page-meta {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: var(--spacing-md);
}

.page-content {
  line-height: 1.6;
  color: var(--text-color);
}

.page-content p {
  margin-bottom: var(--spacing-md);
}

.page-content img {
  max-width: 100%;
  height: auto;
  margin: var(--spacing-md) 0;
  border-radius: var(--border-radius);
}

.page-navigation {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.back-link {
  display: inline-block;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s, transform 0.2s;
}

.back-link:hover {
  color: var(--primary-dark);
  transform: translateX(-3px);
}

.page-not-found {
  text-align: center;
  padding: var(--spacing-xl);
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.page-not-found h2 {
  margin-bottom: var(--spacing-md);
  color: var(--error-color);
}

.page-not-found .back-link {
  margin-top: var(--spacing-lg);
  display: inline-block;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
