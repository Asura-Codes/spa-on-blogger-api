import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { BlogPost } from '@/data/posts';
import { samplePosts } from '@/data/posts';

// Interface for Blogger API response
interface BloggerPost {
  id: string;
  title: string;
  content: string;
  author: {
    displayName: string;
  };
  published: string;
  labels?: string[];
}

export const useBlogStore = defineStore('blog', () => {
  const posts = ref<BlogPost[]>(samplePosts);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const selectedTag = ref<string | null>(null);

  const filteredPosts = computed(() => {
    if (!selectedTag.value) return posts.value;
    return posts.value.filter(post => post.tags.includes(selectedTag.value!));
  });

  const allTags = computed(() => {
    const tagsSet = new Set<string>();
    posts.value.forEach(post => {
      post.tags.forEach(tag => tagsSet.add(tag));
    });
    return Array.from(tagsSet);
  });

  function filterByTag(tag: string | null) {
    selectedTag.value = tag;
  }

  function getPostById(id: number): BlogPost | undefined {
    return posts.value.find(post => post.id === id);
  }

  async function fetchPosts() {
    const apiKey = import.meta.env.VITE_BLOGGER_API_KEY;
    const blogId = import.meta.env.VITE_BLOGGER_BLOG_ID;

    if (!apiKey || !blogId) {
      error.value = 'API key or Blog ID is missing in .env file';
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const url = `https://www.googleapis.com/blogger/v3/blogs/${blogId}/posts?key=${apiKey}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      if (data.items && Array.isArray(data.items)) {
        posts.value = data.items.map((item: BloggerPost) => ({
          id: parseInt(item.id),
          title: item.title,
          content: item.content,
          author: item.author.displayName,
          date: new Date(item.published).toISOString().split('T')[0],
          tags: item.labels || []
        }));
      } else {
        posts.value = [];
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch posts';
      console.error('Error fetching posts:', err);
    } finally {
      isLoading.value = false;
    }
  }

  // Load posts when the store is first instantiated
  fetchPosts();

  return {
    posts,
    filteredPosts,
    allTags,
    selectedTag,
    filterByTag,
    getPostById,
    fetchPosts,
    isLoading,
    error
  };
});
