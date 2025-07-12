<template>
  <div class="blog-post-card">
    <h2 class="post-title">
      <router-link :to="`/post/${post.id}`" class="post-title-link">
        {{ post.title }}
      </router-link>
    </h2>
    <div class="post-meta">
      <span class="post-author">By {{ post.author }}</span>
      <span class="post-date">{{ formatDate(post.date) }}</span>
    </div>
    <div class="post-content" v-html="truncateHTML(post.content)"></div>
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
    <router-link :to="`/post/${post.id}`" class="read-more" aria-label="`Read more about ${post.title}`">
      Read More
    </router-link>
  </div>
</template>

<script setup lang="ts">
import type { BlogPost } from '@/data/posts';
import { useBlogStore } from '@/stores';

defineProps<{
  post: BlogPost
}>();

function truncateHTML(content: string): string {
  // Create a temporary div to parse HTML
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = content;

  // Get the text content to measure length
  const textContent = tempDiv.textContent || tempDiv.innerText || '';

  if (textContent.length <= 150) {
    return content;
  }

  // If content is too long, truncate it
  let truncated = '';
  let currentLength = 0;
  const tags: string[] = [];

  // Simple HTML parser to truncate content while preserving tags
  let inTag = false;
  let currentTag = '';

  for (let i = 0; i < content.length; i++) {
    const char = content[i];

    if (char === '<') {
      inTag = true;
      currentTag = '<';
      continue;
    }

    if (inTag) {
      currentTag += char;
      if (char === '>') {
        inTag = false;

        // Check if it's an opening tag
        if (currentTag.indexOf('</') !== 0) {
          const tagMatch = currentTag.match(/<([a-z0-9]+)[\s>]/i);
          if (tagMatch) {
            tags.push(tagMatch[1]);
          }
        } else {
          // It's a closing tag, remove the last opening tag
          tags.pop();
        }

        truncated += currentTag;
        currentTag = '';
      }
    } else {
      truncated += char;
      currentLength++;

      if (currentLength >= 150) {
        truncated += '...';
        break;
      }
    }
  }

  // Close any unclosed tags
  for (let i = tags.length - 1; i >= 0; i--) {
    truncated += `</${tags[i]}>`;
  }

  return truncated;
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

const blogStore = useBlogStore();

function handleTagClick(tag: string) {
  blogStore.filterByTag(tag);
}
</script>

<style scoped>
.blog-post-card {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  box-shadow: var(--box-shadow);
  transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
  background-color: white;
}

.blog-post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.blog-post-card:focus-within {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

.post-title {
  margin-top: 0;
  margin-bottom: var(--spacing-sm);
  color: var(--text-color);
  font-size: 1.5rem;
}

.post-title-link {
  color: inherit;
  text-decoration: none;
  transition: color var(--transition-speed) ease;
}

.post-title-link:hover,
.post-title-link:focus {
  color: var(--primary-color);
}

.post-meta {
  margin: var(--spacing-sm) 0;
  color: #666;
  font-size: 0.9rem;
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.post-content {
  color: #444;
  line-height: 1.6;
  margin: var(--spacing-md) 0;
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

.read-more {
  display: inline-block;
  margin-top: var(--spacing-sm);
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--transition-speed) ease;
  position: relative;
  padding-right: 1.2em;
}

.read-more::after {
  content: '→';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  transition: transform var(--transition-speed) ease;
}

.read-more:hover::after,
.read-more:focus::after {
  transform: translate(3px, -50%);
}

.read-more:hover,
.read-more:focus {
  color: darken(var(--primary-color), 10%);
}

@media (max-width: 480px) {
  .blog-post-card {
    padding: var(--spacing-md);
  }

  .post-title {
    font-size: 1.25rem;
  }
}
</style>
