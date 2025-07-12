<template>
  <div class="tag-filter" role="region" aria-label="Filter blog posts by tag">
    <h3 id="filter-heading">Filter by Tags</h3>
    <div class="tag-list" role="group" aria-labelledby="filter-heading">
      <button
        class="tag-button"
        :class="{ active: selectedTag === null }"
        @click="clearFilter"
        :aria-pressed="selectedTag === null"
      >
        All Posts
      </button>
      <button
        v-for="tag in tags"
        :key="tag"
        class="tag-button"
        :class="{ active: selectedTag === tag }"
        @click="selectTag(tag)"
        :aria-pressed="selectedTag === tag"
      >
        {{ tag }}
      </button>
    </div>
    <div v-if="selectedTag" class="current-filter">
      <p>Currently showing: <strong>{{ selectedTag }}</strong> <button class="clear-button" @click="clearFilter" aria-label="Clear filter">×</button></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBlogStore } from '@/stores';
import { storeToRefs } from 'pinia';

const blogStore = useBlogStore();
const { allTags, selectedTag } = storeToRefs(blogStore);
const tags = allTags;

function selectTag(tag: string) {
  blogStore.filterByTag(tag);
}

function clearFilter() {
  blogStore.filterByTag(null);
}
</script>

<style scoped>
.tag-filter {
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-md);
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.tag-filter h3 {
  margin-top: 0;
  margin-bottom: var(--spacing-md);
  color: var(--text-color);
  font-size: 1.2rem;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.tag-button {
  background: #f0f0f0;
  border: none;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: 20px;
  font-size: 0.9rem;
  color: #555;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
  font-weight: 500;
}

.tag-button:hover,
.tag-button:focus {
  background: #e0e0e0;
  transform: scale(1.05);
  outline: none;
}

.tag-button.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.current-filter {
  margin-top: var(--spacing-md);
  padding: var(--spacing-sm);
  background-color: #f9f9f9;
  border-radius: var(--border-radius);
  font-size: 0.9rem;
}

.current-filter p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.clear-button {
  background: none;
  border: none;
  color: #999;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 var(--spacing-xs);
  transition: color var(--transition-speed) ease;
}

.clear-button:hover,
.clear-button:focus {
  color: var(--primary-color);
}

@media (max-width: 480px) {
  .tag-list {
    gap: var(--spacing-xs);
  }

  .tag-button {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: 0.8rem;
  }
}
</style>
