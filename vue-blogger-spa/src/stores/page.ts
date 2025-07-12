import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { BlogPage } from '@/data/pages';
import { samplePages } from '@/data/pages';

// Interface for Blogger API page response
interface BloggerPage {
  id: string;
  title: string;
  content: string;
  published: string;
  updated: string;
  links?: Array<{
    rel: string;
    href: string;
    title?: string;
  }>;
}

export const usePageStore = defineStore('page', () => {
  const pages = ref<BlogPage[]>(samplePages);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const getPageById = (id: string): BlogPage | undefined => {
    return pages.value.find(page => page.id === id);
  };

  const getPageByUrl = (url: string): BlogPage | undefined => {
    return pages.value.find(page => page.url === url);
  };

  async function fetchPages() {
    const apiKey = import.meta.env.VITE_BLOGGER_API_KEY;
    const blogId = import.meta.env.VITE_BLOGGER_BLOG_ID;

    if (!apiKey || !blogId) {
      error.value = 'API key or Blog ID is missing in .env file';
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const url = `https://www.googleapis.com/blogger/v3/blogs/${blogId}/pages?key=${apiKey}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      // Log the response to understand its structure
      console.log('Blogger API pages response:', data);

      if (data.items && Array.isArray(data.items)) {
        pages.value = data.items.map((item: BloggerPage) => {
          // Find the alternate link with the URL
          let url = '';

          // Safely access links property with error handling
          if (item.links && Array.isArray(item.links)) {
            const alternateLink = item.links.find(link => link.rel === 'alternate');
            url = alternateLink ? alternateLink.href : '';
          } else {
            console.warn(`Page with id ${item.id} has no links property`, item);
          }

          // Extract the relative path for internal routing
          let relativePath = '';
          if (url) {
            try {
              const urlObj = new URL(url);
              relativePath = urlObj.pathname;
            } catch (e) {
              console.error('Error parsing URL', e);
            }
          }

          return {
            id: item.id || `unknown-${Math.random().toString(36).substring(2, 9)}`,
            title: item.title || 'Untitled Page',
            content: item.content || '<p>No content available</p>',
            published: item.published || new Date().toISOString(),
            updated: item.updated || new Date().toISOString(),
            url: relativePath || `/page/${item.id || 'unknown'}`
          };
        });
      } else {
        pages.value = [];
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch pages';
      error.value = errorMessage;
      console.error('Error fetching pages:', err);
      // Keep using sample data if API fails
      console.log('Using sample data as fallback');
      pages.value = samplePages;
    } finally {
      isLoading.value = false;
    }
  }

  // Load pages when the store is first instantiated
  fetchPages();

  return {
    pages,
    getPageById,
    getPageByUrl,
    fetchPages,
    isLoading,
    error
  };
});
