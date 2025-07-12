<script setup lang="ts">
import BlogPostCard from '@/components/BlogPostCard.vue';
import TagFilter from '@/components/TagFilter.vue';
import PagesWidget from '@/components/PagesWidget.vue';
import { useBlogStore } from '@/stores';
import { storeToRefs } from 'pinia';

const blogStore = useBlogStore();
const { filteredPosts, isLoading, error } = storeToRefs(blogStore);
</script>

<template>
  <div class="home-view">
    <div class="content-layout">
      <main class="main-content">
        <header class="page-header">
          <h1>Blog Posts</h1>
          <p class="subtitle">Explore the latest articles and insights</p>
        </header>

        <TagFilter />

        <div v-if="isLoading" class="loading" role="status" aria-live="polite">
          <div class="loading-spinner"></div>
          <p>Loading posts...</p>
        </div>

        <div v-else-if="error" class="error" role="alert">
          <p>Error: {{ error }}</p>
          <button @click="blogStore.fetchPosts" class="retry-button">
            <span class="retry-icon">↻</span> Try Again
          </button>
        </div>

        <div v-else class="blog-posts">
          <p v-if="filteredPosts.length === 0" class="no-posts" role="status">
            No posts found matching your criteria. Try a different filter.
          </p>

          <BlogPostCard
            v-for="post in filteredPosts"
            :key="post.id"
            :post="post"
          />
        </div>
      </main>

      <aside class="sidebar">
        <PagesWidget />
      </aside>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  max-width: 1000px;
  margin: 0 auto;
}

.content-layout {
  display: flex;
  gap: var(--spacing-xl);
}

.main-content {
  flex: 1;
}

.sidebar {
  width: 280px;
}

@media (max-width: 768px) {
  .content-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    order: -1; /* Show sidebar above content on mobile */
  }
}

.page-header {
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

h1 {
  color: var(--text-color);
  margin-bottom: var(--spacing-xs);
  font-size: 2rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: var(--spacing-lg);
}

.blog-posts {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.loading, .error, .no-posts {
  text-align: center;
  padding: var(--spacing-xl);
  margin: var(--spacing-md) 0;
  border-radius: var(--border-radius);
  background-color: white;
  box-shadow: var(--box-shadow);
}

.loading {
  color: var(--primary-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  color: #dc3545;
  background-color: #fff8f8;
  border: 1px solid #f5c6cb;
}

.retry-button {
  margin-top: var(--spacing-md);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: background-color var(--transition-speed) ease, transform var(--transition-speed) ease;
}

.retry-button:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

.retry-icon {
  font-size: 1.2rem;
}

.no-posts {
  font-style: italic;
  color: #6c757d;
  padding: var(--spacing-xl);
}

@media (max-width: 768px) {
  h1 {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}
</style>
