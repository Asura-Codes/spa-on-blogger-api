<template>
  <div v-if="post" class="post-view">
    <div class="post-header">
      <h1>{{ post.title }}</h1>
      <div class="post-meta">
        <span class="post-author">By {{ post.author }}</span>
        <span class="post-date">{{ formatDate(post.date) }}</span>
      </div>
      <div class="post-tags" aria-label="Post tags">
        <span
          v-for="tag in post.tags"
          :key="tag"
          class="tag"
          @click="handleTagClick(tag)"
          tabindex="0"
          role="button"
          :aria-label="`Filter by tag ${tag}`"
          @keydown.enter="handleTagClick(tag)"
        >
          {{ tag }}
        </span>
      </div>
    </div>

    <div class="post-content" v-html="post.content"></div>

    <div class="post-navigation">
      <router-link to="/" class="back-link">
        &larr; Back to All Posts
      </router-link>
    </div>
  </div>
  <div v-else class="post-not-found">
    <h2>Post Not Found</h2>
    <p>The blog post you're looking for doesn't exist.</p>
    <router-link to="/" class="back-link">
      &larr; Back to All Posts
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useBlogStore } from '@/stores';

const route = useRoute();
const router = useRouter();
const blogStore = useBlogStore();

const postId = computed(() => {
  const id = Number(route.params.id);
  return isNaN(id) ? -1 : id;
});

const post = computed(() => {
  return blogStore.getPostById(postId.value);
});

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

function handleTagClick(tag: string) {
  blogStore.filterByTag(tag);
  router.push('/');
}
</script>

<style scoped>
.post-view {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-md);
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.post-header {
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

.post-meta {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: var(--spacing-md);
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin: var(--spacing-md) 0;
}

.tag {
  background: #f0f0f0;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: 20px;
  font-size: 0.8rem;
  color: #555;
  cursor: pointer;
  transition: background var(--transition-speed) ease, transform var(--transition-speed) ease;
  user-select: none;
}

.tag:hover,
.tag:focus {
  background: #e0e0e0;
  transform: scale(1.05);
  outline: none;
}

.post-content {
  line-height: 1.8;
  color: #444;
  font-size: 1.1rem;
  margin-bottom: var(--spacing-xl);
}

.post-content p {
  margin-bottom: var(--spacing-md);
}

.post-content img {
  max-width: 100%;
  height: auto;
  border-radius: var(--border-radius);
  margin: var(--spacing-md) 0;
}

.post-content a {
  color: var(--primary-color);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color var(--transition-speed) ease;
}

.post-content a:hover,
.post-content a:focus {
  border-color: var(--primary-color);
}

.post-content h2,
.post-content h3 {
  margin-top: var(--spacing-xl);
  margin-bottom: var(--spacing-md);
  color: var(--text-color);
}

.post-navigation {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.back-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--transition-speed) ease;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.back-link:hover,
.back-link:focus {
  color: darken(var(--primary-color), 10%);
}

.post-not-found {
  text-align: center;
  margin: var(--spacing-xl) auto;
  max-width: 500px;
  padding: var(--spacing-lg);
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.post-not-found h2 {
  color: #e74c3c;
  margin-bottom: var(--spacing-md);
}

@media (max-width: 768px) {
  h1 {
    font-size: 1.75rem;
  }

  .post-content {
    font-size: 1rem;
  }
}
</style>
